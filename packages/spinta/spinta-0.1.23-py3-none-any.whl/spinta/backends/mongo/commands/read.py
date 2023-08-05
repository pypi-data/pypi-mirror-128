from starlette.requests import Request

from spinta.accesslog import AccessLog
from spinta.backends import get_select_prop_names
from spinta.backends import get_select_tree
from spinta.compat import urlparams_to_expr
from spinta import commands
from spinta.components import Context, Model, Property, Action, UrlParams
from spinta.renderer import render
from spinta.core.ufuncs import Expr
from spinta.types.datatype import DataType, File, Object
from spinta.exceptions import ItemDoesNotExist, UnavailableSubresource
from spinta.backends.mongo.components import Mongo
from spinta.backends.mongo.commands.query import MongoQueryBuilder


@commands.getone.register(Context, Request, Model, Mongo)
async def getone(
    context: Context,
    request: Request,
    model: Model,
    backend: Mongo,
    *,
    action: Action,
    params: UrlParams,
):
    commands.authorize(context, action, model)

    accesslog = context.get('accesslog')
    accesslog.log(
        model=model.model_type(),
        action=action.value,
        id_=params.pk,
    )

    data = getone(context, model, backend, id_=params.pk)
    select_tree = get_select_tree(context, action, params.select)
    prop_names = get_select_prop_names(context, model, action, select_tree)
    data = commands.prepare_data_for_response(
        context,
        action,
        model,
        backend,
        data,
        select=select_tree,
        prop_names=prop_names,
    )
    return render(context, request, model, params, data, action=action)


@commands.getone.register(Context, Model, Mongo)
def getone(
    context: Context,
    model: Model,
    backend: Mongo,
    *,
    id_: str,
):
    table = backend.db[model.model_type()]
    keys = {k: 1 for k in model.flatprops}
    keys['__id'] = 1
    keys['_id'] = 0
    query = {'__id': id_}
    data = table.find_one(query, keys)
    if data is None:
        raise ItemDoesNotExist(model, id=id_)
    data['_id'] = data['__id']
    data['_type'] = model.model_type()
    return commands.cast_backend_to_python(context, model, backend, data)


@commands.getone.register(Context, Request, Property, DataType, Mongo)
async def getone(
    context: Context,
    request: Request,
    prop: Property,
    dtype: DataType,
    backend: Mongo,
    *,
    action: Action,
    params: UrlParams,
):
    raise UnavailableSubresource(prop=prop.name, prop_type=prop.dtype.name)


@commands.getone.register(Context, Request, Property, (Object, File), Mongo)
async def getone(
    context: Context,
    request: Request,
    prop: Property,
    dtype: (Object, File),
    backend: Mongo,
    *,
    action: Action,
    params: UrlParams,
):
    commands.authorize(context, action, prop)

    accesslog: AccessLog = context.get('accesslog')
    accesslog.log(
        model=prop.model.model_type(),
        prop=prop.place,
        action=action.value,
        id_=params.pk,
    )

    data = getone(context, prop, dtype, backend, id_=params.pk)
    data = commands.prepare_data_for_response(context, Action.GETONE, prop.dtype, backend, data)
    return render(context, request, prop, params, data, action=action)


@commands.getone.register(Context, Property, Object, Mongo)
def getone(
    context: Context,
    prop: Property,
    dtype: Object,
    backend: Mongo,
    *,
    id_: str,
):
    table = backend.db[prop.model.model_type()]
    data = table.find_one({'__id': id_}, {
        '__id': 1,
        '_revision': 1,
        prop.name: 1,
    })
    if data is None:
        raise ItemDoesNotExist(prop, id=id_)
    result = {
        '_id': data['__id'],
        '_revision': data['_revision'],
        '_type': prop.model_type(),
        prop.name: (data.get(prop.name) or {}),
    }
    return commands.cast_backend_to_python(context, prop, backend, result)


@commands.getone.register(Context, Property, File, Mongo)
def getone(
    context: Context,
    prop: Property,
    dtype: File,
    backend: Mongo,
    *,
    id_: str,
):
    table = backend.db[prop.model.model_type()]
    data = table.find_one({'__id': id_}, {
        '__id': 1,
        '_revision': 1,
        prop.name: 1,
    })
    if data is None:
        raise ItemDoesNotExist(prop, id=id_)
    # merge file property data with defaults
    file_data = {
        **{
            '_content_type': None,
            '_id': None,
            '_size': None,
        },
        **data.get(prop.name, {}),
    }
    result = {
        '_id': data['__id'],
        '_revision': data['_revision'],
        '_type': prop.model_type(),
        prop.name: file_data,
    }
    return commands.cast_backend_to_python(context, prop, backend, result)


@commands.getall.register(Context, Request, Model, Mongo)
async def getall(
    context: Context,
    request: Request,
    model: Model,
    backend: Mongo,
    *,
    action: Action,
    params: UrlParams,
):
    commands.authorize(context, action, model)
    expr = urlparams_to_expr(params)
    accesslog = context.get('accesslog')
    accesslog.log(
        model=model.model_type(),
        action=action.value,
    )
    data = commands.getall(context, model, model.backend, query=expr)
    select_tree = get_select_tree(context, action, params.select)
    prop_names = get_select_prop_names(context, model, action, select_tree)
    data = (
        commands.prepare_data_for_response(
            context,
            action,
            model,
            backend,
            row,
            select=select_tree,
            prop_names=prop_names,
        )
        for row in data
    )
    return render(context, request, model, params, data, action=action)


@commands.getall.register(Context, Model, Mongo)
def getall(
    context: Context,
    model: Model,
    backend: Mongo,
    *,
    query: Expr = None,
):
    builder = MongoQueryBuilder(context)
    builder.update(model=model)
    table = backend.db[model.model_type()]
    env = builder.init(backend, table)
    expr = env.resolve(query)
    where = env.execute(expr)
    cursor = env.build(where)
    for row in cursor:
        if '__id' in row:
            row['_id'] = row.pop('__id')
        row['_type'] = model.model_type()
        yield commands.cast_backend_to_python(context, model, backend, row)
