const AWS = require('aws-sdk');
const stepfunctions = new AWS.StepFunctions();
const util = require('util');
const stateMachineArn = "#######";

exports.lambda_handler = (event, context, callback) => {
    const requestId = context.awsRequestId;
    
    console.log("Reading input from event:\n");
    
    const stateMachineExecutionParams = {
        stateMachineArn: stateMachineArn,
        input: JSON.stringify(event),
        name: requestId
    };
    
    //console.log(stateMachineExecutionParams)
    
    stepfunctions.startExecution(stateMachineExecutionParams, (err, data) => {
        if (err) {
            const response = {
                statusCode: 500,
                body : JSON.stringify({
                    message : "There was an error"
                }),
            };
            callback(null, response)
        } else {
            console.log(data);
            const response = {
                statusCode: 200,
                body : JSON.stringify({
                    message : "Works"
                }),
            };
            callback(null, response)    
        }
         
    });
     

};