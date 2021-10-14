function getStoryData(){
return{
  "story":{
    "title":"Untitled",
    "author":"",
    "description":"",
    "metadata":{
      "comments":"",
      "readerStyle":"standard",
      "backDisabled":false,
      "restartDisabled":false
    },
    "nodes":[{
      "id":2,
      "name":"WD",
      "content":{
        "text":"Well Done!",
        "rulesets":[]
      },
      "isStart":false,
      "rules":[]
    },{
      "id":0,
      "name":"Start",
      "content":{
        "text":"This is a sample HypeDyn2 story.",
        "rulesets":[{
          "id":0,
          "name":"new fragment",
          "start":10,
          "end":16,
          "rules":[{
            "id":0,
            "name":"New Rule",
            "stopIfTrue":false,
            "conditionsOp":"or",
            "conditions":[],
            "actions":[{
              "actionType":"LinkTo",
              "params":{
                "node":{
                  "type":"node",
                  "value":1
                }
              }
            }]
          }]
        }]
      },
      "isStart":true,
      "rules":[]
    },{
      "id":1,
      "name":"New Node",
      "content":{
        "text":"It works perfectly!",
        "rulesets":[{
          "id":1,
          "name":"new fragment",
          "start":9,
          "end":19,
          "rules":[{
            "id":1,
            "name":"New Rule",
            "stopIfTrue":false,
            "conditionsOp":"or",
            "conditions":[],
            "actions":[{
              "actionType":"LinkTo",
              "params":{
                "node":{
                  "type":"node",
                  "value":2
                }
              }
            }]
          }]
        }]
      },
      "isStart":false,
      "rules":[]
    }],
    "facts":[],
    "rules":[]
  }
};
};