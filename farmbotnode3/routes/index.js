
/*
 * GET home page.
 */

exports.consoleHome = function (db) {
	return function (req, res) {
		res.render('consoleHome');
	}
};