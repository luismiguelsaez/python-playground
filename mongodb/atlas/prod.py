AWS_PROFILE = "maprod"
AWS_S3_BUCKET_NAME = "s3-steer-dwh-prod"
AWS_REGION = "us-east-2"
AWS_SSM_PREFIX = "/infra/prod/mongoatlas/"

MONGO_ATLAS_ORG_ID = "637e1747c78a470eafc5097"
MONGO_ATLAS_PROJECT_ID = "63971f7be35d0c1f070315ce"
MONGO_ATLAS_FEDERATION_NAME = "prod-dwh"
MONGO_ATLAS_FEDERATED_DB_NAME = "prod-dwh"

triggers = {
    "customers": {
        "type": "DATABASE",
        "name": "customers",
        "source": "infra-prod-mongo01",
        "database": "customers",
        "collection": "Customer",
        "op_types": ["INSERT", "UPDATE", "DELETE", "REPLACE"],
        "function_name": "customers"
    },
    "invoices": {
        "type": "DATABASE",
        "name": "invoices",
        "source": "infra-prod-mongo01",
        "database": "invoices",
        "collection": "Invoices",
        "op_types": ["INSERT", "UPDATE", "DELETE", "REPLACE"],
        "function_name": "invoices"
    },
    "tenants": {
        "type": "DATABASE",
        "name": "tenants",
        "source": "identity-prod-mongo01",
        "database": "identity",
        "collection": "TenantDashboard",
        "op_types": ["INSERT", "UPDATE", "DELETE", "REPLACE"],
        "function_name": "tenants"
    },
    "shops": {
        "type": "DATABASE",
        "name": "shops",
        "source": "identity-prod-mongo01",
        "database": "identity",
        "collection": "ShopDashboard",
        "op_types": ["INSERT", "UPDATE", "DELETE", "REPLACE"],
        "function_name": "shops"
    },
    "service-objects": {
        "type": "DATABASE",
        "name": "service-objects",
        "source": "infra-prod-mongo01",
        "database": "service-objects",
        "collection": "ServiceObject",
        "op_types": ["INSERT", "UPDATE", "DELETE", "REPLACE"],
        "function_name": "service-objects"
    },
    "dump-customers": {
        "type": "SCHEDULED",
        "name": "dump-customers",
        "schedule": "0 */1 * * *",
        "database": "test",
        "service": "dev2-dwh-test",
        "function_name": "dump-customers"
    },
    "dump-invoices": {
        "type": "SCHEDULED",
        "name": "dump-invoices",
        "schedule": "0 */1 * * *",
        "database": "test",
        "service": "dev2-dwh-test",
        "function_name": "dump-invoices"
    },
    "dump-shops": {
        "type": "SCHEDULED",
        "name": "dump-shops",
        "schedule": "0 */1 * * *",
        "database": "test",
        "service": "dev2-dwh-test",
        "function_name": "dump-shops"
    },
    "dump-tenants": {
        "type": "SCHEDULED",
        "name": "dump-tenants",
        "schedule": "0 */1 * * *",
        "database": "test",
        "service": "dev2-dwh-test",
        "function_name": "dump-tenants"
    },
    "dump-service-objects": {
        "type": "SCHEDULED",
        "name": "dump-service-objects",
        "schedule": "0 */1 * * *",
        "database": "test",
        "service": "dev2-dwh-test",
        "function_name": "dump-service-objects"
    }
}

functions = {
        "invoices": {
            "type": "DATABASE",
            "service_name": "infra-prod-mongo01",
            "federated_db_name": "invoices",
            "federated_collection_name": "invoice-updates"
        },
        "customers": {
            "type": "DATABASE",
            "service_name": "infra-prod-mongo01",
            "federated_db_name": "customers",
            "federated_collection_name": "customer-updates"
        },
        "tenants": {
            "type": "DATABASE",
            "service_name": "identity-prod-mongo01",
            "federated_db_name": "identity",
            "federated_collection_name": "tenant-updates"
        },
        "shops": {
            "type": "DATABASE",
            "service_name": "identity-prod-mongo01",
            "federated_db_name": "identity",
            "federated_collection_name": "shop-updates"
        },
        "service-objects": {
            "type": "DATABASE",
            "service_name": "infra-prod-mongo01",
            "federated_db_name": "service-objects",
            "federated_collection_name": "service-object-updates"
        },
        "dump-customers": {
            "type": "SCHEDULED",
            "name": "dump-customers",
            "federation_name": MONGO_ATLAS_FEDERATION_NAME,
            "federated_database_name": MONGO_ATLAS_FEDERATED_DB_NAME,
            "federated_collection_name": "customers"
        },
        "dump-invoices": {
            "type": "SCHEDULED",
            "name": "dump-invoices",
            "federation_name": MONGO_ATLAS_FEDERATION_NAME,
            "federated_database_name": MONGO_ATLAS_FEDERATED_DB_NAME,
            "federated_collection_name": "invoices"
        },
        "dump-shops": {
            "type": "SCHEDULED",
            "name": "dump-shops",
            "federation_name": MONGO_ATLAS_FEDERATION_NAME,
            "federated_database_name": MONGO_ATLAS_FEDERATED_DB_NAME,
            "federated_collection_name": "shops"
        },
        "dump-tenants": {
            "type": "SCHEDULED",
            "name": "dump-tenants",
            "federation_name": MONGO_ATLAS_FEDERATION_NAME,
            "federated_database_name": MONGO_ATLAS_FEDERATED_DB_NAME,
            "federated_collection_name": "tenants"
        },
        "dump-service-objects": {
            "type": "SCHEDULED",
            "name": "dump-service-objects",
            "federation_name": MONGO_ATLAS_FEDERATION_NAME,
            "federated_database_name": MONGO_ATLAS_FEDERATED_DB_NAME,
            "federated_collection_name": "service-objects"
        }
}