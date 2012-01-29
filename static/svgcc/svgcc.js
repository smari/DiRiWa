
//register svg object, and start coloring
var svgDocumentObject;
function registerSvg(o) {
  svgDocumentObject = o.contentDocument;
  colorCountries();
}

function colorCountries() {
  //iterate through countries, and call fillSvgElement for each
  for(var i=0;i<countries.length;i++) {
    if(countries[i] != undefined && countries[i].length == 2) {
      var color = getColor(countries[i][1]);
      var svgo = svgDocumentObject.getElementById(countries[i][0]);
      fillSvgElement(svgo, color, getOpacity(countries[i][1]));
    }
  }
}

function getColor(n) {
  //neutral
  if(n==0)
    return "#ffffff";
  //good
  else if(n>0)
    return "#00ff00";
  //bad
  else if(n<0)
    return "#ff0000";
}

function getOpacity(n) {
  //dont die if error
  if(n>1 || n<-1 || n==0)
    return 1;
  return Math.abs(n);
}

//set fill color and opacity of and svg element and it's children
function fillSvgElement(e, color, opacity) {
  for(var i=0;i<e.children.length;i++) {
    fillSvgElement(e.children[i], color, opacity);
  }
  e.setAttribute("style","fill:"+color+";opacity:"+opacity+";");
}
 
