import asyncio
from sys import argv
from atlas.api import Admin, Appservices
from jinja2 import Template
from config.prod.boston import federation_stores, federation_databases, services, functions, triggers

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
                atlas_appservices.create_app_function(
                    app_id=out_app['_id'],
                    name=function,
                    source=Template(open('functions/templates/' + functions[function]['template']).read()).render(
                        cluster=functions[function]['cluster'],
                        database=functions[function]['database'],
                        collection=functions[function]['collection'],
                        s3_bucket=functions[function]['s3_bucket'] if functions[function]['type'] == 'scheduled' else None,
                        s3_prefix=functions[function]['s3_prefix'] if functions[function]['type'] == 'scheduled' else None,
                        s3_region=functions[function]['s3_region'] if functions[function]['type'] == 'scheduled' else None
                    ),
                )
                    #source=open('functions/boston' + functions[function]['type'] + '-' + functions[function]['name'] + '.js').read())
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