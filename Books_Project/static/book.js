var xhttp = new XMLHttpRequest();
xhttp.open("GET", "http://127.0.0.1:5000/loadfile", true);
xhttp.send();
var obj;
var i=0;
var j=0;
var s=0;
var id_value=0;
xhttp.onload=function(){
obj = JSON.parse(xhttp.responseText);
display(0);
button();

}
function display(a) {
document.getElementById("title").innerHTML=obj.items[a].volumeInfo.title;
document.getElementById("author").innerHTML=obj.items[a].volumeInfo.authors;
document.getElementById("publish").innerHTML=obj.items[a].volumeInfo.publisher;
document.getElementById("yrofpublish").innerHTML=obj.items[a].volumeInfo.publishedDate;
document.getElementById("description").innerHTML=obj.items[a].volumeInfo.description;
document.getElementById("previewlink").innerHTML='<a href='+obj.items[a].volumeInfo.previewLink+'>Book Preview Link</a>';
document.getElementById("image").innerHTML='<img src='+obj.items[a].volumeInfo.imageLinks.smallThumbnail+' alt=pic height=100% width=50% >';
// document.getElementById("price").innerHTML=obj.items[a].saleInfo.retailPrice.amount;
if(obj.items[a].saleInfo.isEbook==true){
	document.getElementById("price").innerHTML=obj.items[a].saleInfo.listPrice.amount;
 	document.getElementById("AddCart").innerHTML='<button onclick=cartadd() style="font-size:20">Add to Cart</button>';

}
else{
	document.getElementById("price").innerHTML='<span>Not Available</span>';
	document.getElementById("AddCart").innerHTML="";
}
}
document.getElementById("logout").innerHTML='<button onclick=logout()>logout</button>';
function button()
{
	n=obj.items.length;
	if(i==0)
	{
		document.getElementById("prev").disabled=true;
	}
	if(i==n-1)
	{
		document.getElementById("nxt").disabled=true;
	}
	if(i>0)
	{
		document.getElementById("prev").disabled=false;
		
	}
	if(i<n-1)
	{
		
		document.getElementById("nxt").disabled=false;	
	}
}
function Next() 
{
	
	
	i++;
	display(i);
	button();
		
}
function Previous() {
	i--;
     
		display(i);
     button();
}

function cartadd() {
	var request= new XMLHttpRequest();
	request.open("GET",'/'+obj.items[i].id+'/'+obj.items[i].saleInfo.listPrice.amount+'/'+obj.items[i].volumeInfo.title, true);
    request.send();
request.onload=function(){
j=JSON.parse(request.responseText);
if(j.flag==6){
	document.getElementById("AddCart").innerHTML="";
	}

document.getElementById("cart_value").innerHTML='<span><img src='+y+' alt="cart value" style="height: 80;width: 80">'+j.s+'   cart </span';

}
}
function logout() {
	var request= new XMLHttpRequest();
	request.open("GET","http://127.0.0.1:5000/logout",true);
	request.send();
request.onload=function(){
document.getElementById("x").innerHTML=request.responseText;
}
}
var y='https://in.all.biz/img/in/service_catalog/6276.jpeg';
document.getElementById("cart_value").innerHTML='<span><img src='+y+' alt="cart value" style="height: 80;width: 80">'+j+'cart </span';
// function checkout_display(a) {
// 	document.getElementById("checkout_name").innerHTML=obj.items[a].volumeInfo.title;
// 	document.getElementById("checkout_author").innerHTML=obj.items[a].volumeInfo.authors;
// 	document.getElementById("checkout_publish").innerHTML=obj.items[a].volumeInfo.publisher;
// 	document.getElementById("checkout_yrofpublish").innerHTML=obj.items[a].volumeInfo.publishedDate;
// 	document.getElementById("checkout_description").innerHTML=obj.items[a].volumeInfo.description;
// 	document.getElementById("checkout_image").innerHTML='<img src='+obj.items[a].volumeInfo.imageLinks.smallThumbnail+' alt=pic height=100% width=50% >';
// }
// function checkout() {
// 	var request= new XMLHttpRequest();
// 	request.open("GET","http://127.0.0.1:5000/checkout",true);
// 	request.send();
// 	request.onload=function(){
// 	document.getElementById("id_value")=id_value;
// }
	
// }