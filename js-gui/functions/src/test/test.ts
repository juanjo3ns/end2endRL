import * as functions from 'firebase-functions';

// // Start writing Firebase Functions
// // https://firebase.google.com/docs/functions/typescript
//
export const test_function = functions.https.onRequest((request, response) => {
 response.send("Hello from test function!");
});
