app_initial_cluster_name = "infra-houston-mongo01"

services = {
    'infra-houston-mongo01': { 'type': 'mongodb-atlas', 'name': 'infra-houston-mongo01', 'cluster_name': 'infra-houston-mongo01' },
    'prod-dwh': { 'type': 'datalake', 'name': 'prod-dwh', 'cluster_name': 'prod-dwh' },
}

# Each function name must match a trigger name
functions = {
    'customer': { 'type': 'database', 'name': 'customer', 'cluster': 'infra-houston-mongo01', 'database': 'customers', 'collection': 'customer-updates', 'template': 'database.js.j2'},
    'invoice': { 'type': 'database', 'name': 'invoice', 'cluster': 'infra-houston-mongo01', 'database': 'invoices', 'collection': 'invoice-updates', 'template': 'database.js.j2'},
    'service_objects': { 'type': 'database', 'name': 'service_objects', 'cluster': 'infra-houston-mongo01', 'database': 'service-objects', 'collection': 'service-object-updates', 'template': 'database.js.j2'},

    'customer-to-s3': { 'type': 'scheduled', 'name': 'customer', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'customers', 'template': 'scheduled.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'customers-houston', 's3_region': 'us-east-2' },
    'invoice-to-s3': { 'type': 'scheduled', 'name': 'invoice', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'invoices', 'template': 'scheduled.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'invoices-houston', 's3_region': 'us-east-2' },
    'service_objects-to-s3': { 'type': 'scheduled', 'name': 'service_objects', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'service-objects', 'template': 'scheduled.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'service-objects-houston', 's3_region': 'us-east-2' },

    'initial-customer': { 'type': 'scheduled', 'name': 'customer', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'customers', 'template': 'scheduled-initial.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'customers-houston/initial/customers', 's3_region': 'us-east-2' },
    'initial-invoice': { 'type': 'scheduled', 'name': 'invoice', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'invoices', 'template': 'scheduled-initial.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'invoices-houston/initial/invoices', 's3_region': 'us-east-2' },
    'initial-service_objects': { 'type': 'scheduled', 'name': 'service_objects', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'service-objects', 'template': 'scheduled-initial.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'service-objects-houston/initial/service-objects', 's3_region': 'us-east-2' },
}

# Each function name must match a trigger name
triggers = {
    'customer': { 'type': 'DATABASE', 'name': 'customer', 'operations': ["INSERT", "UPDATE", "DELETE", "REPLACE"], 'database': 'customers', 'collection': 'Customer', 'service': 'infra-houston-mongo01' },
    'invoice': { 'type': 'DATABASE', 'name': 'invoice', 'operations': ["INSERT", "UPDATE", "DELETE", "REPLACE"], 'database': 'invoices', 'collection': 'Invoice', 'service': 'infra-houston-mongo01' },
    'service_objects': { 'type': 'DATABASE', 'name': 'service_objects', 'operations': ["INSERT", "UPDATE", "DELETE", "REPLACE"], 'database': 'service-objects', 'collection': 'ServiceObject', 'service': 'infra-houston-mongo01' },

    'customer-to-s3': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-houston-mongo01', 'schedule': '0 */1 * * *' },
    'invoice-to-s3': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-houston-mongo01', 'schedule': '0 */1 * * *' },
    'service_objects-to-s3': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-houston-mongo01', 'schedule': '0 */1 * * *' },

    'initial-customer': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-houston-mongo01', 'schedule': '0 */1 * * *' },
    'initial-invoice': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-houston-mongo01', 'schedule': '0 */1 * * *' },
    'initial-service_objects': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-houston-mongo01', 'schedule': '0 */1 * * *' },
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
        "clusterName": "infra-houston-mongo01",
        "name": "prod-infra",
        "projectId": "63c12ecedba0586924108b68",
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