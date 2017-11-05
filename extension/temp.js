$.ajax({
                type: "POST",
                url : "notificationread",
                success : function (data) {
                    if(!data.status)
                        console.log("user not login ");
                    else{
                        var pid = 'notification-card-row' + id;
                        console.log(pid);
                        var a = document.getElementById(pid);
                        console.log(a);
                        $('#'+pid).hide();
                        console.log(a.children[0]);
                        $('#notificationread').prepend(a.children[0]);
                        console.log(a);
                    }
                },
                data: {
                    id: id,
                    csrfmiddlewaretoken: '{{csrf_token}}'
                }
            })