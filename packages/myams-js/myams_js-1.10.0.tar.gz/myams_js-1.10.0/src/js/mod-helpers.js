/* global MyAMS */
/**
 * MyAMS generic helpers
 */

const $ = MyAMS.$;


export const helpers = {

	/**
	 * Click handler used to clear input
	 */
	clearValue: (evt) => {
		const target = $(evt.currentTarget).data('target');
		if (target) {
			$(target).val(null);
		}
	},

	/**
	 * Click handler used to clear datetime input
	 */
	clearDatetimeValue: (evt) => {
		const
			target = $(evt.currentTarget).data('target'),
			picker = $(target).data('datetimepicker');
		if (picker) {
			picker.date(null);
		}
	},

	/**
	 * Select2 change helper
	 */
	select2ChangeHelper: (evt) => {
		const
			source = $(evt.currentTarget),
			data = source.data(),
			target = $(data.amsSelect2HelperTarget);

		switch (data.amsSelect2HelperType) {

			case 'html':
				target.html('<div class="text-center"><i class="fas fa-2x fa-spinner fa-spin"></i></div>');
				const params = {};
				params[data.amsSelect2HelperArgument || 'value'] = source.val();
				$.get(data.amsSelect2HelperUrl, params).then((result) => {
					const callback = MyAMS.core.getFunctionByName(data.amsSelect2HelperCallback) || ((result) => {
						if (result) {
							target.html(result);
							MyAMS.core.initContent(target).then();
						} else {
							target.empty();
						}
					});
					callback(result);
				})
				.catch(() => {
					target.empty();
				});
				break;

			default:
				const callback = data.amsSelect2HelperCallback;
				if (callback) {
					MyAMS.core.executeFunctionByName(callback, source, data);
				}
		}
	},

	/**
	 * Refresh a DOM element with content provided in
	 * the <code>options</code> object.
	 *
	 * @param form: optional parent element
	 * @param options: element properties:
	 *   - object_id: ID of the refreshed element
	 *   - content: new element content
	 */
	refreshElement: (form, options) => {
		return new Promise((resolve, reject) => {
			let element = $(`[id="${options.object_id}"]`);
			MyAMS.core.executeFunctionByName(MyAMS.config.clearContent, document, element).then(() => {
				element.replaceWith($(options.content));
				element = $(`[id="${options.object_id}"]`);
				MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, element).then(() => {
					resolve(element);
				}, reject);
			}, reject);
		});
	},

	/**
	 * Refresh a form widget with content provided in
	 * the <code>options</code> object
	 *
	 * @param form: optional parent form
	 * @param options: updated widget properties:
	 *   - widget_id: ID of the refreshed widget
	 *   - content: new element content
	 */
	refreshWidget: (form, options) => {
		return new Promise((resolve, reject) => {
			let widget = $(`[id="${options.widget_id}"]`),
				group = widget.parents('.widget-group');
			MyAMS.core.executeFunctionByName(MyAMS.config.clearContent, document, group).then(() => {
				group.replaceWith($(options.content));
				widget = $(`[id="${options.widget_id}"]`);
				group = widget.parents('.widget-group');
				MyAMS.core.executeFunctionByName(MyAMS.config.initContent, document, group).then(() => {
					resolve(widget);
				}, reject);
			}, reject);
		});
	},

	/**
	 * Add new row to table
	 *
	 * @param form: optional parent form
	 * @param options: added row properties:
	 *  - content: new row content
	 */
	addTableRow: (form, options) => {
		return new Promise((resolve, reject) => {
			const
				selector = `table[id="${options.table_id}"]`,
				table = $(selector),
				dtTable = table.DataTable();
			let newRow;
			if (options.data) {
				dtTable.rows.add(options.data).draw();
				newRow = $(`tr[id="${options.row_id}"]`, table);
				resolve(newRow);
			} else {
				newRow = $(options.content);
				dtTable.rows.add(newRow).draw();
				MyAMS.core.executeFunctionByName(MyAMS.config.initContent,
					document, newRow).then(() => {
					resolve(newRow);
				}, reject);
			}
		});
	},

	/**
	 * Refresh a table row with content provided in
	 * the <code>options</code> object
	 *
	 * @param form: optional parent form
	 * @param options: updated row properties:
	 *   - row_id: ID of the refreshed row
	 *   - content: new row content
	 */
	refreshTableRow: (form, options) => {
		return new Promise((resolve, reject) => {
			const
				selector = `tr[id="${options.row_id}"]`,
				row = $(selector),
				table = row.parents('table').first();
			if (options.data) {
				if ($.fn.DataTable) {
					const dtTable = table.DataTable();
					if (typeof options.data === 'string') {
						dtTable.row(selector).remove().draw();
						dtTable.row.add($(options.data)).draw();
					} else {
						dtTable.row(selector).data(options.data);
					}
					resolve(row);
				} else {
					reject('No DataTable plug-in available!');
				}
			} else {
				const newRow = $(options.content);
				row.replaceWith(newRow);
				MyAMS.core.executeFunctionByName(MyAMS.config.initContent,
					document, newRow).then(() => {
					resolve(newRow);
				}, reject);
			}
		});
	},

	/**
	 * Refresh a single image with content provided in
	 * the <code>options</code> object.
	 *
	 * @param form: optional parent element
	 * @param options: image properties:
	 *   - image_id: ID of the refreshed image
	 *   - src: new image source URL
	 */
	refreshImage: (form, options) => {
		const image = $(`[id="${options.image_id}"]`);
		image.attr('src', options.src);
	},

	/**
	 * Move given element to the end of it's parent
	 *
	 * @param element: the element to be moved
	 * @returns {*}
	 */
	moveElementToParentEnd: (element) => {
		const parent = element.parent();
		return element.detach()
			.appendTo(parent);
	},

	/**
	 * Toggle dropdown associated with given event target
	 *
	 * @param evt: source event
	 */
	hideDropdown: (evt) => {
		$(evt.target).closest('.dropdown-menu').dropdown('hide');
	}
};


/**
 * Global module initialization
 */
if (window.MyAMS) {
	if (MyAMS.env.bundle) {
		MyAMS.config.modules.push('helpers');
	} else {
		MyAMS.helpers = helpers;
		console.debug("MyAMS: helpers module loaded...");
	}
}
