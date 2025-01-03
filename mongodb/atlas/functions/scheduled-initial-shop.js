exports = async function () {
   const service = context.services.get("prod-dwh");
   const db = service.db("prod-dwh");
   const shops = db.collection("initial-shops");


   console.log("Starting export");
   const pipeline = [
     {
         '$out': {
            's3': {
               'bucket': 's3-steer-dwh-prod',
               'region': 'us-east-2',
               'filename': 'shops/initial/shops',
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
      const result = await shops.aggregate(pipeline).toArray();
      console.log("Aggregation completed successfully:");
     
   } catch (err) {
      console.error("Error during aggregation:", err.message);
   }

   console.log("Export complete");
};