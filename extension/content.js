
$(document).ready(function(){
    chrome.storage.sync.get({blockedposts:{}}, function(item) {
        item['blockedposts'][0] = 1;
        console.log("init blockedposts");
        chrome.storage.sync.set({blockedposts: item['blockedposts']}, function(item) {
        });            
    });
});
chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        console.log("reching here");
        if (request.type == "hello") {
            //chrome.storage.sync.get({posts: {}}, function(item) {
                var ele = document.getElementsByClassName("_5jmm");
                var dataToSend = {};
                for(i = 0; i < ele.length; i++)
                {
                    dataToSend[i] = (ele[i].outerHTML.toString());
                    // if(item['posts'].hasOwnProperty(ele[i].id))
                    // {
                    //     // console.log("already");        
                    // }
                    // else
                    // {
                    //     // console.log("not already");
                    //     dataToSend[j] = (ele[i].outerHTML.toString());
                    //     j = j+1;
                    //     item['posts'][ele[i].id] = 1;
                    // }
                    // chrome.storage.sync.set({'posts': item['posts']}, function(items) {   
                    // });
                }
                console.log('data we are sending');
                // chrome.runtime.sendMessage({}, function(response) {
                userquery = {};
                chrome.storage.sync.get({taglist: []}, function(item) {
                    // console.log("value is ");
                    // console.log(value);
                    for (a in item['taglist'])
                    {
                        userquery[a] = item['taglist'][a];       
                    }
                    console.log(userquery);
                    chrome.storage.sync.get({value:{}}, function(item) {
                        console.log(item);
                        $.ajax({
                            type: "POST",
                            url : "https://bd04563c.ngrok.io/image_to_annotation",
                            data: {
                                fbposts: dataToSend,
                                userquery: userquery,
                            },
                            success : function (data) {
                                blocklist = data['block_list'];
                                console.log(blocklist);
                                console.log("end of ajax");
                                chrome.storage.sync.get({blockedposts:{}}, function(item) {
                                        item['blockedposts'][0] =  item['blockedposts'][0] + blocklist.length;
                                        console.log(item['blockedposts'][0]);
                                        chrome.storage.sync.set({blockedposts: item['blockedposts']}, function(item) {
                                        });
                                        //$('#no_blocked').text("shubz" + item['blockedposts'][0].toString() );      
                                    });             
                                    console.log("value changed");
                                    for (var a in blocklist)
                                    {
                                        $('#'+blocklist[a]).hide();
                                    }
                                },
                            error: function (error) {
                                console.log(error);
                            }
                        });
                        $.ajax({
                            type: "POST",
                            url : "https://bd04563c.ngrok.io/text_to_annotation",
                            data: {
                                fbposts: dataToSend,
                                userquery: userquery,
                            },
                            success : function (data) {
                                blocklist = data['block_list'];
                                console.log(blocklist);
                                console.log("end of ajax");
                                console.log("text_to_annotation");
                                chrome.storage.sync.get({blockedposts:{}}, function(item) {
                                        item['blockedposts'][0] =  item['blockedposts'][0] + blocklist.length;
                                        console.log(item['blockedposts'][0]);
                                        chrome.storage.sync.set({blockedposts: item['blockedposts']}, function(item) {
                                        });
                                        //$('#no_blocked').text("shubz" + item['blockedposts'][0].toString() );      
                                    });             
                                    console.log("value changed");
                                    for (var a in blocklist)
                                    {
                                        $('#'+blocklist[a]).hide();
                                    }
                                },
                            error: function (error) {
                                console.log(error);
                            }
                        });
                    });
                });        
            // });
        }
    }
);

$(document).ready(function(){
    setTimeout(function(){
        var ele = document.getElementsByClassName("_5jmm");
        var dataToSend = {};
        for(i = 0; i < ele.length; i++)
        {
            dataToSend[i] = (ele[i].outerHTML.toString());
            // // console.log("posts are");
            // if(item['posts'].hasOwnProperty(ele[i].id))
            // {
            //     // console.log("already");
            // }
            // else
            // {
            //     // console.log("not already");
            //     dataToSend[j] = (ele[i].outerHTML.toString());
            //     j = j+1;
            //     item['posts'][ele[i].id] = 1;
            // }
            // chrome.storage.sync.set({'posts': item['posts']}, function(items) {   
            // });
        }
        console.log('data we are sending');
        userquery = {};
        chrome.storage.sync.get({taglist: []}, function(item) {   
            for (a in item['taglist'])
            {
                userquery[a] = item['taglist'][a];       
            }
            console.log(userquery);
            chrome.storage.sync.get({value:{}}, function(item) {
                console.log(item);
                $.ajax({
                    type: "POST",
                    url : "https://bd04563c.ngrok.io/image_to_annotation",
                    data: {
                        fbposts: dataToSend,
                        userquery: userquery,
                    },
                    success : function (data) {
                        blocklist = data['block_list'];
                        console.log(blocklist);
                        console.log("end of ajax");
                        chrome.storage.sync.get({blockedposts:{}}, function(item) {
                            item['blockedposts'][0] =  item['blockedposts'][0] + blocklist.length;
                            console.log(item['blockedposts'][0]);
                            chrome.storage.sync.set({blockedposts: item['blockedposts']}, function(item) {
                            });      
                            //$('#no_blocked').text("shubz" + item['blockedposts'][0].toString() );      
                            console.log("value changed");
                            for (var a in blocklist)
                            {
                                $('#'+blocklist[a]).hide();
                            }
                        });
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
                $.ajax({
                    type: "POST",
                    url : "https://bd04563c.ngrok.io/text_to_annotation",
                    data: {
                        fbposts: dataToSend,
                        userquery: userquery,
                    },
                    success : function (data) {
                        blocklist = data['block_list'];
                        console.log(blocklist);
                        console.log("end of ajax");
                        console.log("text_to_annotation");
                        chrome.storage.sync.get({blockedposts:{}}, function(item) {
                            item['blockedposts'][0] =  item['blockedposts'][0] + blocklist.length;
                            console.log(item['blockedposts'][0]);
                            chrome.storage.sync.set({blockedposts: item['blockedposts']}, function(item) {
                            });      
                            //$('#no_blocked').text("shubz" + item['blockedposts'][0].toString() );      
                            console.log("value changed");
                            for (var a in blocklist)
                            {
                                $('#'+blocklist[a]).hide();
                            }
                        });
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            });
        });
            
        setInterval(function(){
        //chrome.storage.sync.get({posts: {}}, function(item) {
                var ele = document.getElementsByClassName("_5jmm");
                var dataToSend = {};
                for(i = 0; i < ele.length; i++)
                {
                    dataToSend[i] = (ele[i].outerHTML.toString());
                    // // console.log("posts are");
                    // if(item['posts'].hasOwnProperty(ele[i].id))
                    // {
                    //     // console.log("already");
                    // }
                    // else
                    // {
                    //     // console.log("not already");
                    //     dataToSend[j] = (ele[i].outerHTML.toString());
                    //     j = j+1;
                    //     item['posts'][ele[i].id] = 1;
                    // }
                    // chrome.storage.sync.set({'posts': item['posts']}, function(items) {   
                    // });
                }
                console.log('data we are sending');
                userquery = {};
                chrome.storage.sync.get({taglist: []}, function(item) {   
                for (a in item['taglist'])
                {
                    userquery[a] = item['taglist'][a];       
                }
                console.log(userquery);
                chrome.storage.sync.get({value:{}}, function(item) {
                    console.log(item);
                    $.ajax({
                        type: "POST",
                        url : "https://bd04563c.ngrok.io/image_to_annotation",
                        data: {
                            fbposts: dataToSend,
                            userquery: userquery,
                        },
                        success : function (data) {
                            blocklist = data['block_list'];
                            console.log(blocklist);
                            console.log("end of ajax");
                            chrome.storage.sync.get({blockedposts:{}}, function(item) {
                                item['blockedposts'][0] =  item['blockedposts'][0] + blocklist.length;
                                console.log(item['blockedposts'][0]);
                                chrome.storage.sync.set({blockedposts: item['blockedposts']}, function(item) {
                                });      
                                //$('#no_blocked').text("shubz" + item['blockedposts'][0].toString() );      
                                console.log("value changed");
                                for (var a in blocklist)
                                {
                                    $('#'+blocklist[a]).hide();
                                }
                            });
                        },
                        error: function (error) {
                            console.log(error);
                        }
                    });
                    $.ajax({
                        type: "POST",
                        url : "https://bd04563c.ngrok.io/text_to_annotation",
                        data: {
                            fbposts: dataToSend,
                            userquery: userquery,
                        },
                        success : function (data) {
                            blocklist = data['block_list'];
                            console.log(blocklist);
                            console.log("end of ajax");
                            console.log("text_to_annotation");
                            chrome.storage.sync.get({blockedposts:{}}, function(item) {
                                item['blockedposts'][0] =  item['blockedposts'][0] + blocklist.length;
                                console.log(item['blockedposts'][0]);
                                chrome.storage.sync.set({blockedposts: item['blockedposts']}, function(item) {
                                });      
                                //$('#no_blocked').text("shubz" + item['blockedposts'][0].toString() );      
                                console.log("value changed");
                                for (var a in blocklist)
                                {
                                    $('#'+blocklist[a]).hide();
                                }
                            });
                        },
                        error: function (error) {
                            console.log(error);
                        }
                    });
                });
            });    
        },20000);
    },4000);
//chrome.storage.sync.get({posts: {}}, function(item) {
        
});