//variable to store current tag entered 
var data = "";
chrome.runtime.onMessage.addListener(function(request, sender,sendResponse) {
    console.log("data from fb in extension");
    sendResponse({userquery:data});
});

document.addEventListener('DOMContentLoaded',function(){
	chrome.tabs.query({active: true, currentWindow: true},function (tabs) {
		tabURL = tabs[0].url;
		fbre = new RegExp("http.*:\/\/.*facebook\..*\/.*");
		twitterre = new RegExp("http.*:\/\/.*twitter\..*\/.*");
	    var fburl = fbre.test(tabURL);
	    var twitterurl = twitterre.test(tabURL);
	    var site=-1;
	    console.log(fburl);
	    console.log(twitterurl);
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
	    console.log("site:");
	    console.log(site);
	    $.ajax({
                type: "POST",
                url: "https://66e9c195.ngrok.io/checklogin",
                success: function(response){
                    if(response.status){
                        $('#login_register').hide();
                        $('#extension').show();
                        $.ajax({
                            type: "GET",
                            url: "https://66e9c195.ngrok.io/fetchtag",
                            data: {
                                site: site
                            },
                            success: function(response){
                                if(response.status){
                                    console.log(response.usertag);
                                    for (var i in response.usertag)
                                    {
                                        var listele = '<li id="'+(response.usertag[i])+(response.usertagtype[i])+'">'+response.usertag[i]+'</li>';
                                        $('#tags').append(listele);
                                    }
                                }
                            },
                            error: function(response){
                                console.log("error in fetch api call");
                            }   
                        });    
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
        if(site>=0)
	    {	        
		    $('#btnSubmit').on('click',function(){
		        tagname = $('#filter').val();
                radiobtnvalue = $("input[name=tag_type]:checked").val()
                dd = $('#dd').val();
                hh = $('#hh').val();
                valid_time = dd*86400 + hh*3600;
                console.log(valid_time);
		        //bring the old list . Append the new tags
		        // chrome.storage.sync.get({taglist: []}, function(item) {
		        //     item['taglist'].push(data);
		        //     //set the new list
		        //     chrome.storage.sync.set({'taglist': item['taglist']}, function(items) {
		        //     });
		        // });

		        $.ajax({
		            type: "GET",
		            url: "https://66e9c195.ngrok.io/addtag",
		            data:{
		                tagname:tagname,
		                tagtype:radiobtnvalue,
		                site:site,
                        valid_time:valid_time
		            },
		            success: function(response){
		                if(response.status){
		                    var listele = '<li id="'+ tagname+radiobtnvalue +'">'+tagname+'</li>';
		                    $('#tags').append(listele);
		                    $('#filter').val(" ");
		                }
		            },
		            error: function(response){
		                console.log("error in addtag api call");
		            }
		        });     
		        //push in frontend
		        
		    });
		}
	});
});
/*    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        var username = $('#login_username').val();
        var password = $('#login_password').val();
        console.log(username,password);
        chrome.tabs.sendMessage(tabs[0].id, {type: "hello",username:username,password:password}, function(response) {
        });
    });*/
/*chrome.storage.sync.get({taglist: []}, function(item) {
    for (var i in item['taglist'])
    {
        var listele = '<li class="removetag" id="'+item['taglist'][i]+'">'+item['taglist'][i]+'</li>';
        $('#tags').append(listele);
    }
}); */
//as popup loads we send a msg asking for posts html

    // chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    //     chrome.tabs.sendMessage(tabs[0].id, {type: "hello",myarg:"myval"}, function(response) {
    //         console.log("inside the response");
    //         console.log(response);
    //     });
    // });


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
    document.getElementById("dashboard").addEventListener("click", dashboard_fun);
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
        url: "https://66e9c195.ngrok.io/register",
        data:{
            username: username,
            password: password
        },
        success: function(data){
            if (data.status)
            {
                $('#register').hide();
                $('#login').hide();
                $('#extension').show();
                chrome.storage.sync.set({'username': username}, function(items) {
	                chrome.storage.sync.set({'password': password}, function(items) {
	                    console.log("set both things");
	                });    
	            });
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
        url: "https://66e9c195.ngrok.io/login",
        data:{
            username: username,
            password: password
        },
        success: function(data){
            $('#login').hide();
            $('#register').hide();
            $('#extension').show();
            chrome.storage.sync.set({'username': username}, function(items) {
                chrome.storage.sync.set({'password': password}, function(items) {
                    console.log("set both things");
                });    
            });
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
        url: "https://66e9c195.ngrok.io/logout",
        success: function(data){
            $('#extension').hide();
            $('#login').show();
            chrome.storage.sync.set({'username': ""}, function(items) {
                chrome.storage.sync.set({'password': ""}, function(items) {
                    console.log("unset both things");
                });    
            });
        },
        error: function(error){
            console.log("error in logout ajax request");
        }
    });
}

function dashboard_fun()
{
    $(document).ready(function(){
        console.log("started in sending login call content.js");    
        chrome.storage.sync.get('username', function(item) {
            var username = item['username'];
            chrome.storage.sync.get('password', function(item) {
                var password = item['password'];
                console.log(username,password);
                window.open("localhost:8000/fb_dashboard?username="+username+"&password="+password,'_blank');
            });
        });
    });
}
//to execute a script at a site 

//var script = 'alert("woow")';
// chrome.tabs.executeScript({
//     code: script
// });