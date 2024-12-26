exports = async function () {
   const service = context.services.get("prod-dwh");
   const db = service.db("prod-dwh");
   const tenants = db.collection("tenants");
   const now = new Date();
   const datePart = `${(now.getMonth() + 1).toString().padStart(2, '0')}-${now.getDate().toString().padStart(2, '0')}-${now.getFullYear()}`;
   const hourPart = `${now.getHours().toString().padStart(2, '0')}-${now.getMinutes().toString().padStart(2, '0')}`;


   console.log("Starting export:", Date.now());
   const pipeline = [
       {
         $match: {
            Updated: {
               $gt: new Date(Date.now() - 1.1 * 60 * 60 * 1000), 
               $lt: new Date() // current time
            }
         }
      },
      {
         '$out': {
            's3': {
               'bucket': 's3-steer-dwh-prod',
               'region': 'us-east-2',
               'filename': `tenants/${datePart}/${hourPart}`,
               'format': {
                  'name': 'json',
                  'maxFileSize': '1GB'
               }
            }
         }
      }
   ];

   try {
      console.log("Executing aggregation pipeline...");
      const result = await tenants.aggregate(pipeline).toArray();
      console.log("Aggregation completed successfully");
     
   } catch (err) {
      console.error("Error during aggregation:", err.message);
   }

   console.log("Export complete");
};
