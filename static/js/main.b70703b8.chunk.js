(this["webpackJsonpproject2-m2-kmp87"]=this["webpackJsonpproject2-m2-kmp87"]||[]).push([[0],{39:function(e,t,a){e.exports=a(88)},44:function(e,t,a){},71:function(e,t){},74:function(e,t,a){},88:function(e,t,a){"use strict";a.r(t);var n=a(0),o=a.n(n),l=a(32),r=a.n(l),c=(a(44),a(38)),s=a(3),i=a(33),m=a.n(i).a.connect("/"),u=(a(74),a(34)),f=a.n(u),g=function(e){var t=e.chat;e.state;return o.a.createElement("div",{className:"h-auto"},t.map((function(e){return o.a.createElement("div",{className:"m-4"},o.a.createElement("div",{className:"flex p-2 flex-col inline-flex mb-3 max-w-md border-opacity-0 rounded-lg overflow-y-auto bg-gray-700"},o.a.createElement("div",{className:"flex space-x-2"},o.a.createElement("img",{className:"rounded-full w-8 h-8",src:e.profilePic,alt:"profile pic"}),o.a.createElement("div",{className:"h-auto font-extrabold text-white text-md mr-2 font-sans"},e.name)),o.a.createElement("div",null,o.a.createElement("div",{className:"font-mono mt-1 text-gray-200 text-base h-auto "},f()(e.message)))))})))},d=function(e){var t=e.props;return o.a.createElement("div",{className:"flex flex-row place-items-auto items-center"},o.a.createElement("div",{className:"flex-1 p-3 m-3 font-serif text-white text-xl font-extrabold"},"#general"),o.a.createElement("div",{className:"flex-1 items-center text-center text-c p-3 m-3 font-serif text-gray-400 text-xl "},t[1]),o.a.createElement("div",{className:"flex-1 text-right font-serif text-white text-xl p-3 m-3"},o.a.createElement("span",{className:"text-green-500 text-xl"},"\u25cf "),"Online:"," ",t[0]))},p=function(e){var t=e.onTextChange,a=e.onMessageSubmit,n=e.message;return o.a.createElement("div",{className:"flex w-full m-2 justify-center rounded-lg border-2 border-grey-600 "},o.a.createElement("button",{type:"button",className:"hover:bg-gray-200 text-3xl text-grey bg-gray-300 px-3 border-r-2",onClick:function(e){""!==n&&a(e)}},"+"),o.a.createElement("input",{type:"text",className:"w-full mr-4 p-4 bg-gray-300 focus:bg-white",placeholder:"Message to #general",value:n,onChange:function(e){t(e.target.value)},onKeyPress:function(e){"Enter"===e.key&&""!==n&&a(e)},required:!0}))},x=a(35),v=a.n(x),b=function(e){var t=e.setAccountInfo,a=e.setLoginStatus,n=e.setState;return o.a.createElement("div",{className:"align-middle"},o.a.createElement(v.a,{appId:"856995921505171",autoLoad:!1,fields:"name,email,picture",callback:function(e){a(!1),n({name:e.name,message:""}),t({email:e.email,profilePic:e.picture.data.url}),m.emit("update_total_users",e.email)},onFailure:function(){return alert("Failed to login")},cookie:!1}))},E=a(36),h=a.n(E),j=a(37),N=a.n(j),w=function(e){var t=e.setAccountInfo,a=e.setLoginStatus,n=e.setState;return o.a.createElement("div",{className:"align-middle"},o.a.createElement(h.a,{clientId:"955471402983-pei3u5jmjvjq6uiruv8dv4mdlch9ebig.apps.googleusercontent.com",buttonText:"Login",onSuccess:function(e){a(!1),n({name:e.profileObj.name,message:""}),t({email:e.profileObj.email,profilePic:e.profileObj.imageUrl}),m.emit("update_total_users",e.profileObj.email)},cookiePolicy:"single_host_origin"},o.a.createElement(N.a,{name:"google"}),o.a.createElement("span",null," Login with Google")))},y=function(e){var t=e.setAccountInfo,a=e.setLoginStatus,n=e.setState;return o.a.createElement(o.a.Fragment,null,o.a.createElement("div",{className:"bg-gray-200 w-screen h-screen flex flex-col justify-center items-center"},o.a.createElement("h1",{className:"font-hairline mb-6 font-extrabold text-4xl text-left"},"Login to ChatApp"),o.a.createElement("div",{className:"flex-col flex "},o.a.createElement(w,{setAccountInfo:t,setLoginStatus:a,setState:n}),o.a.createElement(b,{setAccountInfo:t,setLoginStatus:a,setState:n}))))};var S=function(){var e=Object(n.useState)({name:"",message:""}),t=Object(s.a)(e,2),a=t[0],l=t[1],r=Object(n.useState)({email:"",profilePic:""}),i=Object(s.a)(r,2),u=i[0],f=i[1],x=Object(n.useState)([]),v=Object(s.a)(x,2),b=v[0],E=v[1],h=Object(n.useState)(0),j=Object(s.a)(h,2),N=j[0],w=j[1],S=Object(n.useState)(!0),O=Object(s.a)(S,2),k=O[0],L=O[1];Object(n.useEffect)((function(){return m.on("on_connect",(function(e){E(e.messages)})),m.on("update_users",(function(e){w(e.totalUsers)})),m.on("message_sent",(function(e){var t=e.message,a=t.name,n=t.message,o=t.email,l=t.profilePic;return E((function(e){return[].concat(Object(c.a)(e),[{name:a,message:n,email:o,profilePic:l}])}))})),m.on("on_disconnect",(function(e){w(e.totalUsers)})),function(){m&&m.removeAllListeners()}}),[]);var P=function(e){l({name:a.name,message:e})},_=function(e){e.preventDefault();var t=a.name,n=a.message,o=u.email,r=u.profilePic;m.emit("message",{name:t,message:n,email:o,profilePic:r}),l({name:t,message:""})};return o.a.createElement("div",null,k?o.a.createElement(y,{setAccountInfo:f,setLoginStatus:L,setState:l}):o.a.createElement("div",{className:"flex flex-col h-screen overflow-x-hidden "},o.a.createElement("div",{className:"mb-3 bg-gradient-to-b from-gray-900"},o.a.createElement(d,{props:[N,a.name]})),o.a.createElement("div",{className:"flex flex-1 flex-col-reverse overflow-y-auto"},o.a.createElement(g,{chat:b,state:a})),o.a.createElement(p,{onTextChange:P,onMessageSubmit:_,message:a.message})))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));r.a.render(o.a.createElement(o.a.StrictMode,null,o.a.createElement(S,null)),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()})).catch((function(e){console.error(e.message)}))}},[[39,1,2]]]);
//# sourceMappingURL=main.b70703b8.chunk.js.map