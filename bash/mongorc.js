var prompt = function() {
    var host = db.serverStatus().host;
    var tm = new Date()
    var m = tm.getMonth();
    if (m < 10) m = '0' + m;
    var d = tm.getDate();
    if (d < 10) d = '0' + d;
    var h = tm.getHours();
    if (h < 10) h = '0' + h;
    var mi= tm.getMinutes();
    if (mi < 10) mi = '0' + mi;
    var s = tm.getSeconds();
    if (s < 10) s = '0' + s;
    var tminfo = "[" + m + '-' + d + ' ' + h + ':' + mi + ':' + s + ']-';
    var prmpt = tminfo +  host + "@"+ db +"-MongDB> ";
    return prmpt; 
}
