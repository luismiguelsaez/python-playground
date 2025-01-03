exports = async function () {
   const service = context.services.get("prod-dwh");
   const db = service.db("prod-dwh");
   const customers = db.collection("initial-invoices");


   console.log("Starting export");
   const pipeline = [
     {
         '$out': {
            's3': {
               'bucket': 's3-steer-dwh-prod',
               'region': 'us-east-2',
               'filename': 'invoices/initial/invoices',
               'format': {
                  'name': 'json',
                  'maxFileSize': '100GB'
                }
            }
         }
      }
   ];

   try {
      console.log("Executing aggregation pipeline...");
      const result = await customers.aggregate(pipeline).toArray();
      console.log("Aggregation completed successfully:");
     
   } catch (err) {
      console.error("Error during aggregation:", err.message);
   }

   console.log("Export complete");
};