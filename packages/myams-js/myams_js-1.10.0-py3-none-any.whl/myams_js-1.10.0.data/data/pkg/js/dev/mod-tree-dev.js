(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(["exports"], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports);
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports);
    global.modTree = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.tree = void 0;

  function _createForOfIteratorHelper(o, allowArrayLike) { var it; if (typeof Symbol === "undefined" || o[Symbol.iterator] == null) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = o[Symbol.iterator](); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it.return != null) it.return(); } finally { if (didErr) throw err; } } }; }

  function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

  function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

  /* global MyAMS */

  /**
   * MyAMS tree management
   */
  var $ = MyAMS.$;
  var tree = {
    /**
     * Open/close tree node inside a table
     */
    switchTreeNode: function switchTreeNode(evt) {
      var removeChildNodes = function removeChildNodes(node_id) {
        $("tr[data-ams-tree-node-parent-id=\"".concat(node_id, "\"]")).each(function (idx, elt) {
          var row = $(elt);
          removeChildNodes(row.data('ams-tree-node-id'));
          dtTable.row(row).remove().draw();
        });
      };

      var node = $(evt.currentTarget),
          switcher = $('i.switch', node),
          tr = node.parents('tr').first(),
          table = tr.parents('table').first(),
          dtTable = table.DataTable();
      node.tooltip('hide');

      if (switcher.hasClass('minus')) {
        removeChildNodes(tr.data('ams-tree-node-id'));
        MyAMS.core.switchIcon(switcher, 'minus-square', 'plus-square', 'far');
        switcher.removeClass('minus');
      } else {
        var location = tr.data('ams-location') || table.data('ams-location') || '',
            treeNodesTarget = tr.data('ams-tree-nodes-target') || table.data('ams-tree-nodes-target') || 'get-tree-nodes.json',
            sourceName = tr.data('ams-element-name');
        MyAMS.core.switchIcon(switcher, 'plus-square', 'cog', 'fas');

        MyAMS.require('ajax').then(function () {
          MyAMS.ajax.post(location + '/' + sourceName + '/' + treeNodesTarget, {
            can_sort: !$('td.sorter', tr).is(':empty')
          }).then(function (result) {
            if (result.length > 0) {
              var newRow,
                  oldRow = tr;

              var _iterator = _createForOfIteratorHelper(result),
                  _step;

              try {
                for (_iterator.s(); !(_step = _iterator.n()).done;) {
                  var row = _step.value;
                  newRow = $(row);
                  dtTable.row.add(newRow).draw();
                  oldRow = newRow;
                  MyAMS.core.initContent(newRow).then();
                }
              } catch (err) {
                _iterator.e(err);
              } finally {
                _iterator.f();
              }
            }

            MyAMS.core.switchIcon(switcher, 'cog', 'minus-square', 'far');
            switcher.addClass('minus');
          });
        });
      }
    },

    /**
     * Open close all tree nodes
     */
    switchTree: function switchTree(evt) {
      var node = $(evt.currentTarget),
          switcher = $('i.switch', node),
          th = node.parents('th'),
          table = th.parents('table').first(),
          tableID = table.data('ams-tree-node-id'),
          dtTable = table.DataTable();
      node.tooltip('hide');

      if (switcher.hasClass('minus')) {
        $('tr[data-ams-tree-node-parent-id]').filter("tr[data-ams-tree-node-parent-id!=\"".concat(tableID, "\"]")).each(function (idx, elt) {
          dtTable.row(elt).remove().draw();
        });
        $('i.switch', table).each(function (idx, elt) {
          MyAMS.core.switchIcon($(elt), 'minus-square', 'plus-square', 'far');
          $(elt).removeClass('minus');
        });
      } else {
        var location = table.data('ams-location') || '',
            target = table.data('ams-tree-nodes-target') || 'get-tree.json',
            tr = $('tbody tr', table.first());
        MyAMS.core.switchIcon(switcher, 'plus-square', 'cog', 'fas');

        MyAMS.require('ajax').then(function () {
          MyAMS.ajax.post("".concat(location, "/").concat(target), {
            can_sort: !$('td.sorter', tr).is(':empty')
          }).then(function (result) {
            $("tr[data-ams-tree-node-id]", table).each(function (idx, elt) {
              dtTable.row(elt).remove().draw();
            });
            $(result).each(function (idx, elt) {
              var newRow = $(elt);
              dtTable.row.add(newRow).draw();
            });
            MyAMS.core.initContent(table).then();
            MyAMS.core.switchIcon(switcher, 'cog', 'minus-square', 'far');
            switcher.addClass('minus');
          });
        });
      }
    },

    /**
     * Custom tree element delete callback
     *
     * @param form: source form, which can be null if callback wasn't triggered from a form
     * @param options: callback options
     */
    deleteElement: function deleteElement(form, options) {
      console.debug(options);
      var nodeId = options.node_id;

      if (nodeId) {
        $("tr[data-ams-tree-node-parent-id=\"".concat(nodeId, "\"]")).each(function (idx, elt) {
          var table = $(elt).parents('table'),
              dtTable = table.DataTable();
          dtTable.row(elt).remove().draw();
        });
      }
    },

    /**
     * Sort and re-parent tree elements
     */
    sortTree: function sortTree(evt, details) {
      var table = $(evt.target),
          dtTable = table.DataTable(),
          data = $(table).data();
      var target = data.amsReorderUrl;

      if (target) {
        // Disable row click handler
        var row = $(data.amsReorderSource.node);
        row.data('ams-disabled-handlers', 'click');

        try {
          // Get root ID
          var tableID = row.parents('table').first().data('ams-tree-node-id'); // Get moved row ID

          var rowID = row.data('ams-tree-node-id');
          var rowParentID = row.data('ams-tree-node-parent-id'); // Get new parent ID

          var parent = row.prev('tr');
          var parentID, switcher, action;

          if (parent.exists()) {
            // Move below an existing row
            parentID = parent.data('ams-tree-node-id'); // Check switcher state

            switcher = $('.switch', parent);

            if (switcher.hasClass('minus')) {
              // Opened folder: move as child
              if (rowParentID === parentID) {
                // Don't change parent
                action = 'reorder';
              } else {
                // Change parent
                action = 'reparent';
              }
            } else {
              // Closed folder or simple item: move as sibling
              parentID = parent.data('ams-tree-node-parent-id');

              if (rowParentID === parentID) {
                // Don't change parent
                action = 'reorder';
              } else {
                // Change parent
                action = 'reparent';
              }
            }
          } else {
            // Move to site root
            parentID = tableID;
            switcher = null;

            if (rowParentID === parentID) {
              // Already child of site root
              action = 'reorder';
            } else {
              // Move from inner folder to site root
              action = 'reparent';
            }
          } // Call ordering target


          var localTarget = MyAMS.core.getFunctionByName(target);

          if (typeof localTarget === 'function') {
            localTarget.call(table, dnd_table, post_data);
          } else {
            if (!target.startsWith(window.location.protocol)) {
              var location = data.amsLocation;

              if (location) {
                target = location + '/' + target;
              }
            }

            var postData = {
              action: action,
              child: rowID,
              parent: parentID,
              order: JSON.stringify($('tr[data-ams-tree-node-id]').listattr('data-ams-tree-node-id')),
              can_sort: !$('td.sorter', row).is(':empty')
            };

            MyAMS.require('ajax').then(function () {
              MyAMS.ajax.post(target, postData).then(function (result) {
                var removeRow = function removeRow(rowID) {
                  var row = $("tr[data-ams-tree-node-id=\"".concat(rowID, "\"]"));
                  dtTable.row(row).remove().draw();
                };

                var removeChildRows = function removeChildRows(rowID) {
                  var childs = $("tr[data-ams-tree-node-parent-id=\"".concat(rowID, "\"]"));
                  childs.each(function (idx, elt) {
                    var childRow = $(elt),
                        childID = childRow.attr('data-ams-tree-node-id');
                    removeChildRows(childID);
                    dtTable.row(childRow).remove().draw();
                  });
                };

                if (result.status) {
                  MyAMS.ajax.handleJSON(result);
                } else {
                  // Remove parent row if changed parent
                  if (postData.action === 'reparent') {
                    removeRow(parentID);
                  } // Remove moved row children


                  removeChildRows(parentID);
                  removeChildRows(rowID);
                  dtTable.row(row).remove().draw();
                  var newRow, oldRow;

                  var _iterator2 = _createForOfIteratorHelper(result),
                      _step2;

                  try {
                    for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
                      var resultRow = _step2.value;
                      newRow = $(resultRow);
                      oldRow = $("tr[id=\"".concat(newRow.attr('id'), "\"]"));
                      dtTable.row(oldRow).remove().draw();
                      dtTable.row.add(newRow).draw();
                      MyAMS.core.initContent(newRow).then();
                    }
                  } catch (err) {
                    _iterator2.e(err);
                  } finally {
                    _iterator2.f();
                  }
                }
              });
            });
          }
        } finally {
          // Restore row click handler
          setTimeout(function () {
            $(row).removeData('ams-disabled-handlers');
          }, 50);
        }
      }

      return false;
    }
  };
  /**
   * Global module initialization
   */

  _exports.tree = tree;

  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('tree');
    } else {
      MyAMS.tree = tree;
      console.debug("MyAMS: tree module loaded...");
    }
  }
});
//# sourceMappingURL=mod-tree-dev.js.map
