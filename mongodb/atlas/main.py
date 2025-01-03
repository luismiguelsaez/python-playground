import asyncio
from sys import argv
from atlas.api import Admin, Appservices

async def main():
    public_key = argv[1]
    private_key = argv[2]
    project_id = argv[3]

    if not public_key or not private_key or not project_id:
        print("Usage: python test.py <public_key> <private_key> <project_id>")
        exit(1)

    atlas_admin = Admin(
            public_key=public_key,
            private_key=private_key,
            project_id=project_id
    )

    atlas_appservices = Appservices(
            public_key=public_key,
            private_key=private_key,
            project_id=project_id
    )

    services = {
        'infra-prod-mongo01': { 'type': 'mongodb-atlas', 'name': 'infra-prod-mongo01', 'cluster_name': 'infra-prod-mongo01' },
        'identity-prod-mongo01': { 'type': 'mongodb-atlas', 'name': 'identity-prod-mongo01', 'cluster_name': 'identity-prod-mongo01' },
        'prod-dwh': { 'type': 'datalake', 'name': 'prod-dwh', 'cluster_name': 'prod-dwh' },
    }

    # Each function name must match a trigger name
    functions = {
        'customer': { 'type': 'database', 'name': 'customer', 'source': 'exports = function() { return "hello world!"; }' },
        'invoice': { 'type': 'database', 'name': 'invoice', 'source': 'exports = function() { return "hello world!"; }' },
        'tenant': { 'type': 'database', 'name': 'invoice', 'source': 'exports = function() { return "hello world!"; }' },
        'shop': { 'type': 'database', 'name': 'shop', 'source': 'exports = function() { return "hello world!"; }' },
        'service_objects': { 'type': 'database', 'name': 'service_objects', 'source': 'exports = function() { return "hello world!"; }' },

        'customer-to-s3': { 'type': 'scheduled', 'name': 'customer', 'source': 'exports = function() { return "hello world!"; }' },
        'invoice-to-s3': { 'type': 'scheduled', 'name': 'invoice', 'source': 'exports = function() { return "hello world!"; }' },
        'tenant-to-s3': { 'type': 'scheduled', 'name': 'invoice', 'source': 'exports = function() { return "hello world!"; }' },
        'shop-to-s3': { 'type': 'scheduled', 'name': 'shop', 'source': 'exports = function() { return "hello world!"; }' },
        'service_objects-to-s3': { 'type': 'scheduled', 'name': 'service_objects', 'source': 'exports = function() { return "hello world!"; }' },

        'initial-customer': { 'type': 'scheduled', 'name': 'customer', 'source': 'exports = function() { return "hello world!"; }' },
        'initial-invoice': { 'type': 'scheduled', 'name': 'invoice', 'source': 'exports = function() { return "hello world!"; }' },
        'initial-tenant': { 'type': 'scheduled', 'name': 'invoice', 'source': 'exports = function() { return "hello world!"; }' },
        'initial-shop': { 'type': 'scheduled', 'name': 'shop', 'source': 'exports = function() { return "hello world!"; }' },
        'initial-service_objects': { 'type': 'scheduled', 'name': 'service_objects', 'source': 'exports = function() { return "hello world!"; }' },
    }

    # Each function name must match a trigger name
    triggers = {
        'customer': { 'type': 'DATABASE', 'name': 'customer', 'operations': ["INSERT", "UPDATE", "DELETE", "REPLACE"], 'database': 'customers', 'collection': 'Customer', 'service': 'infra-prod-mongo01' },
        'invoice': { 'type': 'DATABASE', 'name': 'invoice', 'operations': ["INSERT", "UPDATE", "DELETE", "REPLACE"], 'database': 'invoices', 'collection': 'Invoice', 'service': 'infra-prod-mongo01' },
        'tenant': { 'type': 'DATABASE', 'name': 'tenant', 'operations': ["INSERT", "UPDATE", "DELETE", "REPLACE"], 'database': 'identity', 'collection': 'TenantDashboard', 'service': 'identity-prod-mongo01' },
        'shop': { 'type': 'DATABASE', 'name': 'shop', 'operations': ["INSERT", "UPDATE", "DELETE", "REPLACE"], 'database': 'identity', 'collection': 'ShopDashboard', 'service': 'identity-prod-mongo01' },
        'service_objects': { 'type': 'DATABASE', 'name': 'service_objects', 'operations': ["INSERT", "UPDATE", "DELETE", "REPLACE"], 'database': 'service-objects', 'collection': 'ServiceObject', 'service': 'infra-prod-mongo01' },

        'customer-to-s3': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-prod-mongo01', 'schedule': '0 */1 * * *' },
        'invoice-to-s3': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-prod-mongo01', 'schedule': '0 */1 * * *' },
        'tenant-to-s3': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'identity-prod-mongo01', 'schedule': '0 */1 * * *' },
        'shop-to-s3': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'identity-prod-mongo01', 'schedule': '0 */1 * * *' },
        'service_objects-to-s3': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-prod-mongo01', 'schedule': '0 */1 * * *' },

        'initial-customer': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-prod-mongo01', 'schedule': '0 */1 * * *' },
        'initial-invoice': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-prod-mongo01', 'schedule': '0 */1 * * *' },
        'initial-tenant': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'identity-prod-mongo01', 'schedule': '0 */1 * * *' },
        'initial-shop': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'identity-prod-mongo01', 'schedule': '0 */1 * * *' },
        'initial-service_objects': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-prod-mongo01', 'schedule': '0 */1 * * *' },
    }

    federation_databases = [
        {
            "name": "prod-dwh",
            "views": [],
            "collections": [
                {
                    "name": "customers",
                    "dataSources": [
                        {
                            "collection": "customer-updates",
                            "database": "customers",
                            "storeName": "prod-infra"
                        }
                    ]
                },
                {
                    "name": "initial-customers",
                    "dataSources": [
                        {
                            "collection": "Customer",
                            "database": "customers",
                            "storeName": "prod-infra"
                        }
                    ]
                },
                {
                    "name": "initial-invoices",
                    "dataSources": [
                        {
                            "collection": "Invoice",
                            "database": "invoices",
                            "storeName": "prod-infra"
                        }
                    ]
                },
                {
                    "name": "initial-tenants",
                    "dataSources": [
                        {
                            "collection": "TenantDashboard",
                            "database": "identity",
                            "storeName": "prod-identity"
                        }
                    ]
                },
                {
                    "name": "initial-shops",
                    "dataSources": [
                        {
                            "collection": "ShopDashboard",
                            "database": "identity",
                            "storeName": "prod-identity"
                        }
                    ]
                },
                {
                    "name": "invoices",
                    "dataSources": [
                        {
                            "collection": "invoice-updates",
                            "database": "invoices",
                            "storeName": "prod-infra"
                        }
                    ]
                },
                {
                    "name": "shops",
                    "dataSources": [
                        {
                            "collection": "shop-updates",
                            "database": "identity",
                            "storeName": "prod-identity"
                        }
                    ]
                },
                {
                    "name": "tenants",
                    "dataSources": [
                        {
                            "collection": "tenant-updates",
                            "database": "identity",
                            "storeName": "prod-identity"
                        }
                    ]
                },
                {
                    "name": "initial-service-objects",
                    "dataSources": [
                        {
                            "collection": "ServiceObject",
                            "database": "service-objects",
                            "storeName": "prod-infra"
                        }
                    ]
                },
                {
                    "name": "service-objects",
                    "dataSources": [
                        {
                            "collection": "service-object-updates",
                            "database": "service-objects",
                            "storeName": "prod-infra"
                        }
                    ]
                }
            ],
        }
    ]

    federation_stores = [
        {
            "clusterName": "infra-prod-mongo01",
            "name": "prod-infra",
            "projectId": project_id,
            "provider": "atlas",
            "readPreference": {
                "mode": "secondary"
            }
        },
        {
            "clusterName": "identity-prod-mongo01",
            "name": "prod-identity",
            "projectId": project_id,
            "provider": "atlas",
            "readPreference": {
                "mode": "secondary"
            }
        },
        {
            "bucket": "s3-steer-dwh-prod",
            "delimiter": "/",
            "name": "s3-steer-dwh-prod",
            "provider": "s3",
            "region": "us-east-2"
        }
    ]

    # Get Cloud Providers
    res_providers, out_providers = await atlas_admin.get_cloud_provider_access(provider_name='AWS')
    print(f"Providers: {out_providers}")
    exit(1) if not res_providers else None

    res_data_federations, out_data_federations = await atlas_admin.create_data_federation(
        name='prod-dwh',
        databases=federation_databases,
        stores=federation_stores,
        role_id=out_providers[0]['roleId'],
        test_bucket='s3-steer-dwh-prod'
    )
    print(f"Data Federations: {out_data_federations}")
    exit(1) if not res_data_federations else None

    # Create App
    res_app, out_app = await atlas_appservices.create_app(app_name='Triggers', cluster_name='infra-prod-mongo01')
 
    print(f"App: {out_app}")
    exit(1) if not res_app else None

    # Create Services
    async with asyncio.TaskGroup() as tg:
        services_tasks = {
            service: tg.create_task(atlas_appservices.create_app_service(app_id=out_app['_id'], name=services[service]['name'], cluster_name=services[service]['cluster_name'], type=services[service]['type']))
            for service in services
        }

    for task in services_tasks:
        res_service, out_service = await services_tasks[task]
        print(f"Service: {out_service}")
        exit(1) if not res_service else None

    res_app_services, out_app_services = await atlas_appservices.get_app_services(app_id=out_app['_id'])
    print(f"App Services: {out_app_services}")
    exit(1) if not res_app_services else None

    # Link Data Sources
    data_sources = [
        {'name': services[service]['name'], 'type': services[service]['type'], 'config': {'clusterName': services[service]['cluster_name']}}
        for service in services
    ]

    res_link_serivces, out_link_services = await atlas_appservices.create_app_service_link(app_id=out_app['_id'], data_sources=data_sources)
    print(f"Link Services: {out_link_services}")
    exit(1) if not res_link_serivces else None

    # Create Functions
    async with asyncio.TaskGroup() as tg:
        tasks_functions = {
            function: tg.create_task(
                atlas_appservices.create_app_function(app_id=out_app['_id'], name=function, source=open('functions/' + functions[function]['type'] + '-' + functions[function]['name'] + '.js').read())
            )
            for function in functions
        }
    for task in tasks_functions:
        res_function, out_function = await tasks_functions[task]
        print(f"Function [{task}]: {out_function}")
        exit(1) if not res_function else None

    # Create Triggers
    async with asyncio.TaskGroup() as tg:
        tasks_triggers_database = {
            trigger: tg.create_task(atlas_appservices.create_app_trigger(
                trigger_name=trigger,
                app_id=out_app['_id'],
                operations=triggers[trigger]['operations'],
                database=triggers[trigger]['database'],
                collection=triggers[trigger]['collection'],
                service_id=services_tasks[triggers[trigger]['service']].result()[1]['_id'],
                function_id=tasks_functions[trigger].result()[1]['_id'],
                type=triggers[trigger]['type']
            ))
            for trigger in triggers if triggers[trigger]['type'] == 'DATABASE'
        }
        tasks_triggers_scheduled = {
                trigger: tg.create_task(atlas_appservices.create_app_trigger(
                    trigger_name=trigger,
                    app_id=out_app['_id'],
                    schedule=triggers[trigger]['schedule'],
                    function_id=tasks_functions[trigger].result()[1]['_id'],
                    type=triggers[trigger]['type']
                ))
                for trigger in triggers if triggers[trigger]['type'] == 'SCHEDULED'
        }
        tasks = {**tasks_triggers_database, **tasks_triggers_scheduled}
    for task in tasks:
        res_trigger, out_trigger = await tasks[task]
        print(f"Trigger [{task}]: {out_trigger}")
        exit(1) if not res_trigger else None

if __name__ == '__main__':
    asyncio.run(main())