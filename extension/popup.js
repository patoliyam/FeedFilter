var data = "";
//listener : it runs when we get data from content.js(fb)
chrome.runtime.onMessage.addListener(function(request, sender,sendResponse) {
    console.log("data from fb in extension");
    // var obj = request;
    sendResponse({userquery:data});

});

document.addEventListener('DOMContentLoaded',function(){
    if($('#image_moderation').prop("checked")==true)
    {
        chrome.storage.sync.get({value:{}}, function(item) {
            console.log("checked");
            item['value'][0] = 1;
            chrome.storage.sync.set({value: item['value']}, function(item) {
                console.log(item);
            });            
        }); 
    }
    else
    {
        chrome.storage.sync.get({value:{}}, function(item) {
            console.log("not checked");
            item['value'][0] = 0;
            chrome.storage.sync.set({value: item['value']}, function(item) {
                console.log(item);
            });            
        });            
    }

    chrome.storage.sync.get({taglist: []}, function(item) {
        for (var i in item['taglist'])
        {
            var listele = '<li class="removetag" id="'+item['taglist'][i]+'">'+item['taglist'][i]+'</li>';
            $('#tags').append(listele);
        }
    }); 
    //as popup loads we send a msg asking for posts html
    $('#btnSubmit').on('click',function(){
        data = $('#filter').val();
        //bring the old list . Append the new tags
        chrome.storage.sync.get({taglist: []}, function(item) {
            item['taglist'].push(data);
            //set the new list
            chrome.storage.sync.set({'taglist': item['taglist']}, function(items) {
            });
        });     
        //push in frontend
        var listele = '<li class="removetag" id="'+ data +'">'+data+'</li>';
        $('#tags').append(listele);
        // console.log(data);
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {type: "hello"}, function(response) {
                console.log("inside the response");
                //console.log(response);s
            });
        }); 
    });


});

// $(document).ready(function(){
//     setInterval(function(){
//         console.log("printing");
//         chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
//             chrome.tabs.sendMessage(tabs[0].id, {type: "hello"}, function(response) {
//                 console.log("inside the response");
//                 //console.log(response);s
//             });
//         }); 
//     }, 10000);
// });

$(document).ready(function(){
    $('.removetag').click(function(){
        var value = $(this).text();
        $('#'+value).remove();
        chrome.storage.sync.get({taglist: []}, function(item) {
            var index = item['taglist'].indexOf(value);
            item['taglist'].splice(index, 1);
            //set the new list
            chrome.storage.sync.set({'taglist': item['taglist']}, function(items) {
            });
        }); 
    });
});


$(document).ready(function() {
    $('#image_moderation').change(function() {
        if($(this).is(":checked")) {
            chrome.storage.sync.get({value:{}}, function(item) {
                item['value'][0] = 1;
                chrome.storage.sync.set({value: item['value']}, function(item) {
                });            
            });
        }
        else
        {
            chrome.storage.sync.get({value:{}}, function(item) {
                item['value'][0] = 0;
                chrome.storage.sync.set({value: item['value']}, function(item) {
                });            
            });
        }
    });
});






    //to execute a script at a site 

    //var script = 'alert("woow")';
    // chrome.tabs.executeScript({
    //     code: script
    // });