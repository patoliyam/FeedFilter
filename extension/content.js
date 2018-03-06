$(document).ready(function(){
    tabURL = location;
    fbre = new RegExp("http.*:\/\/.*facebook\..*\/.*");
    twitterre = new RegExp("http.*:\/\/.*twitter\..*\/.*");
    var fburl = fbre.test(tabURL);
    var twitterurl = twitterre.test(tabURL);
    var site=-1;
    if(fburl)
    {
        site = 0;
    }
    else if(twitterurl)
    {
        site = 1;
    }
    else
    {
        site = -1;
    }
    console.log("site");
    console.log(site);
    if(site>=0)
    {
        setTimeout(function(){
            sendpostandhide(site);
            text(site);  
            name(site);
        },4000);        
    }
});

// $(document).ready(function(){
//     console.log("started in sending login call content.js");    
//     chrome.storage.sync.get('username', function(item) {
//         var username = item['username'];
//         chrome.storage.sync.get('password', function(item) {
//             var password = item['password'];
//             console.log(username,password);
//         });
//     });
// });

/*chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        // console.log("reching here");
        if (request.type == "hello") {
            // sendpostandhide();
            console.log("message handler was working");
        }
    }
);*/

function sendpostandhide(site){
    var dataToSend = {};
    // var idlist = [];
    var idlist = {};
    if (site == 0)
    {
        var ele = document.getElementsByClassName("_5jmm");
        for(i = 0; i < ele.length; i++)
        {
            dataToSend[i] = (ele[i].outerHTML.toString());
        }
    }
    else if(site == 1)
    {
        var ele = document.getElementsByClassName("AdaptiveMedia-photoContainer js-adaptive-photo ");
        var ele2 = document.getElementsByClassName("js-stream-item stream-item stream-item");
        for(i = 0; i < Math.min(ele.length,ele2.length); i++)
        {
            // idlist.push(ele2[i].id);
            idlist[i] = (ele2[i].id);
            dataToSend[i] = (ele[i].outerHTML.toString());
        }
    }

    // userquery = {};
    console.log('data we are sending is : ');
    console.log(dataToSend);
    chrome.storage.sync.get({textmodvalue:{}}, function(item) {
        var textmodvalue = item['textmodvalue'][0];
        chrome.storage.sync.get({imagemodvalue:{}}, function(item) {
            var imagemodvalue = item['imagemodvalue'][0];
            $.ajax({
                type: "POST",
                url : "https://66e9c195.ngrok.io/image_to_annotation",
                data: {
                    fbposts: dataToSend,
                    // userquery: userquery,
                    textmodvalue: textmodvalue,
                    idlist: idlist,
                    imagemodvalue: imagemodvalue,
                    site: site
                },
                success : function (data) {
                    blocklist = data['block_list'];
                    console.log("blacklist is");
                    console.log(blocklist);
                    console.log("end of ajax i_to_a");
                    for (var a in blocklist)
                    {
                        if(site==0)
                        {
                            $('#'+blocklist[a]).hide();
                        }
                        else if(site == 1)
                        {
                            $('#'+blocklist[a]).remove();
                        }

                    }
                },
                error: function (error) {
                    console.log(error);
                }
            }).then(function(){
                tabURL = location;
                fbre = new RegExp("http.*:\/\/.*facebook\..*\/.*");
                twitterre = new RegExp("http.*:\/\/.*twitter\..*\/.*");
                var fburl = fbre.test(tabURL);
                var twitterurl = twitterre.test(tabURL);
                var site=-1;
                if(fburl)
                {
                    site = 0;
                }
                else if(twitterurl)
                {
                    site = 1;
                }
                else
                {
                    site = -1;
                }
                if(site>=0)
                {
                    sendpostandhide(site);
                }
            });
        });
    });
}

function text(site)
{
    var dataToSend = {};
    if (site == 0)
    {    
        var ele = document.getElementsByClassName("_5jmm");
        for(i = 0; i < ele.length; i++)
        {
            dataToSend[i] = (ele[i].outerHTML.toString());
        }
    }
    else if(site == 1)
    {
        var ele = document.getElementsByClassName("content");
        for(i = 0; i < ele.length; i++)
        {
            dataToSend[i] = (ele[i].outerHTML.toString());
        }
    }
    // userquery = {};
    console.log('data we are sending is : ');
    console.log(dataToSend);    
    chrome.storage.sync.get({textmodvalue:{}}, function(item) {
        var textmodvalue = item['textmodvalue'][0];
        chrome.storage.sync.get({imagemodvalue:{}}, function(item) {
            var imagemodvalue = item['imagemodvalue'][0];
            $.ajax({
                type: "POST",
                url : "https://66e9c195.ngrok.io/text_to_annotation",
                data: {
                    fbposts: dataToSend,
                    // userquery: userquery,
                    textmodvalue: textmodvalue,
                    imagemodvalue: imagemodvalue,
                    site: site
                },
                success : function (data) {
                    blocklist = data['block_list'];
                    console.log("blocklist is");
                    console.log(blocklist);
                    console.log("end of ajax t_to_a");
                    for (var a in blocklist)
                    {
                        $('#'+blocklist[a]).hide();
                    }
                },
                error: function (error) {
                    console.log(error);
                }
            }).then(function(){
                tabURL = location;
                fbre = new RegExp("http.*:\/\/.*facebook\..*\/.*");
                twitterre = new RegExp("http.*:\/\/.*twitter\..*\/.*");
                var fburl = fbre.test(tabURL);
                var twitterurl = twitterre.test(tabURL);
                var site=-1;
                if(fburl)
                {
                    site = 0;
                }
                else if(twitterurl)
                {
                    site = 1;
                }
                else
                {
                    site = -1;
                }
                if(site>=0)
                {
                    text(site);
                }
            });;
        });
    });
}


function name(site){
    var dataToSend = {};
    if (site == 0)
    {
        var ele = document.getElementsByClassName("_5jmm");
        for(i = 0; i < ele.length; i++)
        {    
            dataToSend[i] = (ele[i].outerHTML.toString());
        }
    }
    else if(site == 1)
    {
        var ele = document.getElementsByClassName("content");
        for(i = 0; i < ele.length; i++)
        {
            dataToSend[i] = (ele[i].outerHTML.toString());
        }
    }
    // userquery = {};
    console.log('data we are sending is : ');
    console.log(dataToSend);    
    $.ajax({
        type: "POST",
        url : "https://66e9c195.ngrok.io/name_filter",
        data: {
            fbposts: dataToSend,
            // userquery: userquery,
            site: site
        },
        success : function (data) {
            blocklist = data['block_list'];
            console.log("blocklist is");
            console.log(blocklist);
            console.log("end of ajax name_filter");
            for (var a in blocklist)
            {
                $('#'+blocklist[a]).hide();
            }
        },
        error: function (error) {
            console.log(error);
        }
    }).then(function(){
        tabURL = location;
        fbre = new RegExp("http.*:\/\/.*facebook\..*\/.*");
        twitterre = new RegExp("http.*:\/\/.*twitter\..*\/.*");
        var fburl = fbre.test(tabURL);
        var twitterurl = twitterre.test(tabURL);
        var site=-1;
        if(fburl){
            site = 0;
        }
        else if(twitterurl){
            site = 1;
        }
        else{
            site = -1;
        }
        if(site>=0)
        {
            name(site);
        }
    });;
}