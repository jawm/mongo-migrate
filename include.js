function i(variable){
	if (typeof variable == 'number'){
		return NumberInt(variable);
	}
	return variable.map(function(s){
		return i(s);
	});
}
