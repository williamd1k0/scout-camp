
function getUrlSearch(arg){
    var query = window.location.search.substring(1);
    var args = query.split("&");
    var argsobject = {};
    for (var i = 0; i < args.length; i++){
        var pair = args[i].split("=");
        if(typeof arg === 'undefined'){
            argsobject[pair[0]] = pair[1];
        }else if(pair[0] == arg){
            return pair[1];
        }
    }
    return argsobject;
}

const $_GET = getUrlSearch();
