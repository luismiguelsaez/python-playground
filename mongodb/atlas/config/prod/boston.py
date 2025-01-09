services = {
    'infra-prod-mongo01': { 'type': 'mongodb-atlas', 'name': 'infra-prod-mongo01', 'cluster_name': 'infra-prod-mongo01' },
    'identity-prod-mongo01': { 'type': 'mongodb-atlas', 'name': 'identity-prod-mongo01', 'cluster_name': 'identity-prod-mongo01' },
    'prod-dwh': { 'type': 'datalake', 'name': 'prod-dwh', 'cluster_name': 'prod-dwh' },
}

# Each function name must match a trigger name
functions = {
    'customer': { 'type': 'database', 'name': 'customer', 'cluster': 'infra-prod-mongo01', 'database': 'customers', 'collection': 'customer-updates', 'template': 'database.js.j2'},
    'invoice': { 'type': 'database', 'name': 'invoice', 'cluster': 'infra-prod-mongo01', 'database': 'invoices', 'collection': 'invoice-updates', 'template': 'database.js.j2'},
    'tenant': { 'type': 'database', 'name': 'invoice', 'cluster': 'identity-prod-mongo01', 'database': 'identity', 'collection': 'tenant-updates', 'template': 'database.js.j2'},
    'shop': { 'type': 'database', 'name': 'shop', 'cluster': 'identity-prod-mongo01', 'database': 'identity', 'collection': 'shop-updates', 'template': 'database.js.j2'},
    'service_objects': { 'type': 'database', 'name': 'service_objects', 'cluster': 'infra-prod-mongo01', 'database': 'service-objects', 'collection': 'service-object-updates', 'template': 'database.js.j2'},

    'customer-to-s3': { 'type': 'scheduled', 'name': 'customer', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'customers', 'template': 'scheduled.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'boston/customers', 's3_region': 'us-east-2' },
    'invoice-to-s3': { 'type': 'scheduled', 'name': 'invoice', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'invoices', 'template': 'scheduled.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'boston/invoices', 's3_region': 'us-east-2' },
    'tenant-to-s3': { 'type': 'scheduled', 'name': 'invoice', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'tenants', 'template': 'scheduled.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'boston/tenants', 's3_region': 'us-east-2' },
    'shop-to-s3': { 'type': 'scheduled', 'name': 'shop', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'shops', 'template': 'scheduled.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'boston/shops', 's3_region': 'us-east-2' },
    'service_objects-to-s3': { 'type': 'scheduled', 'name': 'service_objects', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'service-objects', 'template': 'scheduled.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'boston/service-objects', 's3_region': 'us-east-2' },

    'initial-customer': { 'type': 'scheduled', 'name': 'customer', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'customers', 'template': 'scheduled-initial.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'boston/customers/initial/customers', 's3_region': 'us-east-2' },
    'initial-invoice': { 'type': 'scheduled', 'name': 'invoice', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'invoices', 'template': 'scheduled-initial.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'boston/invoices/initial/invoices', 's3_region': 'us-east-2' },
    'initial-tenant': { 'type': 'scheduled', 'name': 'invoice', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'tenants', 'template': 'scheduled-initial.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'boston/tenants/initial/tenants', 's3_region': 'us-east-2' },
    'initial-shop': { 'type': 'scheduled', 'name': 'shop', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'shops', 'template': 'scheduled-initial.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'boston/shops/initial/shops', 's3_region': 'us-east-2' },
    'initial-service_objects': { 'type': 'scheduled', 'name': 'service_objects', 'cluster': 'prod-dwh', 'database': 'prod-dwh', 'collection': 'service-objects', 'template': 'scheduled-initial.js.j2', 's3_bucket': 's3-steer-dwh-prod', 's3_prefix': 'boston/service-objects/initial/service-objects', 's3_region': 'us-east-2' },
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
        "projectId": "63971f7be35d0c1f070315ce",
        "provider": "atlas",
        "readPreference": {
            "mode": "secondary"
        }
    },
    {
        "clusterName": "identity-prod-mongo01",
        "name": "prod-identity",
        "projectId": "63971f7be35d0c1f070315ce",
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
