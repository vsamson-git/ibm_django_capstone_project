/**
 * Get all dealerships
 */

 const { CloudantV1 } = require('@ibm-cloud/cloudant');
 const { IamAuthenticator } = require('ibm-cloud-sdk-core');
 
 module.exports.handler = async function main(event) {
     const authenticator = new IamAuthenticator({ apikey: process.env.IAM_API_KEY })
     const cloudant = CloudantV1.newInstance({
     authenticator: authenticator
   });
     cloudant.setServiceUrl(process.env.COUCH_URL);
     
     try {
       let dealerships = await cloudant.postAllDocs({
       db: 'dealerships',
       includeDocs: true,
       inclusiveEnd: false
     });
     dealerships = dealerships.result.rows.map(row => row.doc)
       if (event.queryStringParameters !== null && event.queryStringParameters !== undefined) {
         let query = event.queryStringParameters
         if (query.state !== null && query.state !== undefined) {
           dealerships = dealerships.filter(val => val.state == query.state)
         }
       }
       
     if (dealerships.length) {
       return { dealerships }
     }
     else {
      return {statusCode: 404, error: "The database is empty" }; 
     }
     
   } catch (error) {
     return { error: error.description , statusCode: 500 };
   }
 
   
 }
 
 