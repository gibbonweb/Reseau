window.addEvent('domready', function(){
	$('admin-toggle').addEvent('click', function(event){
    	event.stop(); //Prevents the browser from following the link.
		$('admin-add-post').setStyle('display',('block'==$('admin-add-post').getStyle('display'))?'none':'block');
	});
	console.log("dom ready");
});