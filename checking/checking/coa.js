frappe.provide("erpnext.financial_statements");

erpnext.financial_statements = {
	"formatter": function(row, cell, value, columnDef, dataContext, default_formatter) {
		if (columnDef.df.fieldname=="account") {
			value = dataContext.account_name;

			columnDef.df.link_onclick =
				"erpnext.financial_statements.open_general_ledger(" + JSON.stringify(dataContext) + ")";
			columnDef.df.is_tree = true;
		}

		value = default_formatter(row, cell, value, columnDef, dataContext);

		if (!dataContext.parent_account) {
			var $value = $(value).css("font-weight", "bold");
			if (dataContext.warn_if_negative && dataContext[columnDef.df.fieldname] < 0) {
				$value.addClass("text-danger");
			}

			value = $value.wrap("<p></p>").parent().html();
		}

		return value;
	},

	"tree": true,
	"name_field": "account",
	"parent_field": "parent_account",
	"initial_depth": 3,

};
