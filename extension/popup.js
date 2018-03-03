//variable to store current tag entered 
var data = "";
//listener : it runs when we get data from content.js(fb)
chrome.runtime.onMessage.addListener(function(request, sender,sendResponse) {
    console.log("data from fb in extension");
    // var obj = request;
    sendResponse({userquery:data});

});

document.addEventListener('DOMContentLoaded',function(){
    
    $.ajax({
        type: "POST",
        url: "https://d771d65c.ngrok.io/checklogin",
        success: function(response){
            if(response.status){
                $('#login_register').hide();
                $('#extension').show();
            }
            else{
                $('#extension').hide();
                $('#login').show();
            }
        },
        error: function(response){
            console.log("error in api call");
        }
    });

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

//clicking on any tag will remove the tag from taglist and from frontend too
$(document).ready(function(){
    
    document.getElementById("show_register").addEventListener("click", show_register_form);
    document.getElementById("register_btn").addEventListener("click", register_fun);
    document.getElementById("login_btn").addEventListener("click", login_fun);
    document.getElementById("logout_btn").addEventListener("click", logout_fun);

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

$(document).ready(function(){
    chrome.storage.sync.get({imagemodvalue: {}}, function(item) {
        console.log("printed value of imagemodvale");
        console.log(item['imagemodvalue']);
        if(item['imagemodvalue'][0]==1){
            document.getElementById("image_moderation").checked = true;
        }else{
            document.getElementById("image_moderation").checked = false;
        }

    });
    chrome.storage.sync.get({textmodvalue: {}}, function(item) {
        console.log("printed value of textmodvale");
        console.log(item['textmodvalue']);
        if(item['textmodvalue'][0]==1){
            document.getElementById("text_moderation").checked = true;
        }else{
            document.getElementById("text_moderation").checked = false;
        }
    });
});



$(document).ready(function() {
    $('#image_moderation').change(function() {
        if($(this).is(":checked")) {
            console.log("checked imagemodvalue");
            chrome.storage.sync.get({imagemodvalue:{}}, function(item) {
                item['imagemodvalue'][0] = 1;
                chrome.storage.sync.set({imagemodvalue: item['imagemodvalue']}, function(item) {
                });            
            });
        }
        else
        {
            console.log("unchecked imagemodvalue");
            chrome.storage.sync.get({imagemodvalue:{}}, function(item) {
                item['imagemodvalue'][0] = 0;
                chrome.storage.sync.set({imagemodvalue: item['imagemodvalue']}, function(item) {
                });            
            });
        }
    });
});
$(document).ready(function() {
    $('#text_moderation').change(function() {
        if($(this).is(":checked")) {
            console.log("checked textmodvalue");
            chrome.storage.sync.get({textmodvalue:{}}, function(item) {
                item['textmodvalue'][0] = 1;
                chrome.storage.sync.set({textmodvalue: item['textmodvalue']}, function(item) {
                });            
            });
        }
        else
        {
            console.log("unchecked textmodvalue");
            chrome.storage.sync.get({textmodvalue:{}}, function(item) {
                item['textmodvalue'][0] = 0;
                chrome.storage.sync.set({textmodvalue: item['textmodvalue']}, function(item) {
                });            
            });
        }
    });
});





function show_register_form()
{
    $('#login').hide();
    $('#register').show();
}

function register_fun()
{
    var username = $('#register_username').val();
    var password = $('#register_password').val();

    $.ajax({
        type: "POST",
        url: "https://d771d65c.ngrok.io/register",
        data:{
            username: username,
            password: password
        },
        success: function(data){
            if (data.status)
            {
                $('#login_register').hide();
                $('#extension').show();
            }
            else
            {
                console.log("api error");
                alert("use another username");
            }
        },
        error: function(error){
            console.log("error in register ajax request");
        }
    });
}

function login_fun()
{
    var username = $('#login_username').val();
    var password = $('#login_password').val();

    $.ajax({
        type: "POST",
        url: "https://d771d65c.ngrok.io/login",
        data:{
            username: username,
            password: password
        },
        success: function(data){
            $('#login_register').hide();
            $('#extension').show();
        },
        error: function(error){
            console.log("error in register ajax request");
        }
    });   
}

function logout_fun()
{
    $.ajax({
        type: "POST",
        url: "https://d771d65c.ngrok.io/logout",
        success: function(data){
            console.log("here");
            $('#extension').hide();
            $('#login_register').show();
        },
        error: function(error){
            console.log("error in logout ajax request");
        }
    });
}

//to execute a script at a site 

//var script = 'alert("woow")';
// chrome.tabs.executeScript({
//     code: script
// });