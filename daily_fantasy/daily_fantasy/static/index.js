var dataView;
var grid;
var contests = [];
var data = [];

//  {id: "sel", name: "#", field: "num", behavior: "select", cssClass: "cell-selection", width: 40, cannotTriggerInsert: true, resizable: false, selectable: false },


  var titleFormatter = function ( row, cell, value, columnDef, dataContext ) {
        return '<a href=' + dataContext['url'] + ' target="_blank" >' + value + '</a>';
    };

  var joinFormatter = function ( row, cell, value, columnDef, dataContext ) {
        return '<a class = "join" href="' + value + '" target="_blank">' + "Join!" + '</a>';
    };

var columns = [

  {id: "sport", name: "Sport", field: "sport", cssClass: "cell-title", sortable: true},
  {id: "site", name: "Site", field: "site",  cssClass: "cell-title", sortable: true},
  {id: "title", name: "Title", field: "title", width: 300,  cssClass: "cell-title", sortable: true, formatter: titleFormatter},
  {id: "buyin", name: "Buy-In", field: "buyin",  sortable: true},
  {id: "payout", name: "Payout", field: "payout",  sortable: true},
  {id: "entries", name: "Entries", field: "entries",  sortable: true},
  {id: "size", name: "Size", field: "size",  sortable: true},
  {id: "url", name: "Join", field: "url", width: 60, sortable: false, formatter: joinFormatter}

//  {id: "start", name: "Start", field: "start", minWidth: 60, sortable: true}
];

var options = {
  editable: false,
  enableAddRow: false,
  enableCellNavigation: false,
  asyncEditorLoading: true,
  forceFitColumns: true,
  topPanelHeight: 25,
  headerRowHeight: 0,
  rowHeight: 50
};

var sortcol = "title";
var sortdir = 1;
var percentCompleteThreshold = 0;
var searchString = "";

function requiredFieldValidator(value) {
  if (value == null || value == undefined || !value.length) {
    return {valid: false, msg: "This is a required field"};
  }
  else {
    return {valid: true, msg: null};
  }
}

function myFilter(item, args) {
  if (item["percentComplete"] < args.percentCompleteThreshold) {
    return false;
  }

  if (args.searchString != "" &&
      item["title"].toLowerCase().indexOf(args.searchString.toLowerCase()) == -1) {
    return false;
  }

  return true;
}

function percentCompleteSort(a, b) {
  return a["percentComplete"] - b["percentComplete"];
}

function comparer(a, b) {
  var x = a[sortcol], y = b[sortcol];
  var numerical = ["buyin", "payout"]
  if (numerical.indexOf(sortcol) > -1) {
      return (x == y ? 0 : (parseFloat(x) > parseFloat(y) ? 1 : -1));
  }
  else{
      return (x == y ? 0 : (x > y ? 1 : -1));
  }
}

function toggleFilterRow() {
  grid.setTopPanelVisibility(!grid.getOptions().showTopPanel);
}

$(".grid-header .ui-icon")
        .addClass("ui-state-default ui-corner-all")
        .mouseover(function (e) {
          $(e.target).addClass("ui-state-hover")
        })
        .mouseout(function (e) {
          $(e.target).removeClass("ui-state-hover")
        });

$(function () {
//  //prepare the data
//  for (var i = 0; i < 50000; i++) {
//    var d = (data[i] = {});
//    d["id"] = "id_" + i;
//    d["num"] = i;
//    d["title"] = "Task " + i;
//    d["duration"] = "5 days";
//    d["percentComplete"] = Math.round(Math.random() * 100);
//    d["start"] = "01/01/2009";
//    d["finish"] = "01/05/2009";
//    d["effortDriven"] = (i % 5 == 0);
//  }

  $.ajax({
        url: 'rawdata',
        dataType: 'json',
        global: false,
        async: false,
        success: function(data){
         for (i = 0; i < data.length; i++){
             contests.push(data[i]["fields"]);
         }
        }
   });

  //prepare the data
  for (var i = 0; i < contests.length; i++) {
    data[i] = {};
    data[i]["id"] = "id_" + i;
    data[i]["sport"] = contests[i]["sport"];
    data[i]["site"] = contests[i]["site"];
    data[i]["title"] = contests[i]["title"];
    data[i]["buyin"] = contests[i]["buyin"];
    data[i]["payout"] = contests[i]["payout"];
    data[i]["entries"] = contests[i]["entries"];
    data[i]["size"] = contests[i]["size"];
    data[i]["url"] = contests[i]["url"];
  }

  dataView = new Slick.Data.DataView({ inlineFilters: true });
  grid = new Slick.Grid("#myGrid", dataView, columns, options);
  //grid.setSelectionModel(new Slick.RowSelectionModel());

  var pager = new Slick.Controls.Pager(dataView, grid, $("#pager"));
  var columnpicker = new Slick.Controls.ColumnPicker(columns, grid, options);


  // move the filter panel defined in a hidden div into grid top panel
  $("#inlineFilterPanel")
      .appendTo(grid.getTopPanel())
      .show();

  grid.onCellChange.subscribe(function (e, args) {
    dataView.updateItem(args.item.id, args.item);
  });

  grid.onAddNewRow.subscribe(function (e, args) {
    var item = {"num": data.length, "id": "new_" + (Math.round(Math.random() * 10000)), "title": "New task", "duration": "1 day", "percentComplete": 0, "start": "01/01/2009", "finish": "01/01/2009", "effortDriven": false};
    $.extend(item, args.item);
    dataView.addItem(item);
  });

  grid.onKeyDown.subscribe(function (e) {
    // select all rows on ctrl-a
    if (e.which != 65 || !e.ctrlKey) {
      return false;
    }

    var rows = [];
    for (var i = 0; i < dataView.getLength(); i++) {
      rows.push(i);
    }

    grid.setSelectedRows(rows);
    e.preventDefault();
  });

  grid.onSort.subscribe(function (e, args) {
    sortdir = args.sortAsc ? 1 : -1;
    sortcol = args.sortCol.field;

    if ( ($.browser.msie && $.browser.version <= 8) ) {
      // using temporary Object.prototype.toString override
      // more limited and does lexicographic sort only by default, but can be much faster

      var percentCompleteValueFn = function () {
        var val = this["percentComplete"];
        if (val < 10) {
          return "00" + val;
        } else if (val < 100) {
          return "0" + val;
        } else {
          return val;
        }
      };

      // use numeric sort of % and lexicographic for everything else

      dataView.fastSort((sortcol == "percentComplete") ? percentCompleteValueFn : sortcol, args.sortAsc);
    } else {
      // using native sort with comparer
      // preferred method but can be very slow in IE with huge datasets
      dataView.sort(comparer, args.sortAsc);
    }
  });

  // wire up model events to drive the grid
  dataView.onRowCountChanged.subscribe(function (e, args) {
    grid.updateRowCount();
    grid.render();
  });

  dataView.onRowsChanged.subscribe(function (e, args) {
    grid.invalidateRows(args.rows);
    grid.render();
  });

  dataView.onPagingInfoChanged.subscribe(function (e, pagingInfo) {
    var isLastPage = pagingInfo.pageNum == pagingInfo.totalPages - 1;
    var enableAddRow = isLastPage || pagingInfo.pageSize == 0;
    var options = grid.getOptions();

    if (options.enableAddRow != enableAddRow) {
      grid.setOptions({enableAddRow: enableAddRow});
    }
  });


  var h_runfilters = null;

  // wire up the slider to apply the filter to the model
  $("#pcSlider,#pcSlider2").slider({
    "range": "min",
    "slide": function (event, ui) {
      Slick.GlobalEditorLock.cancelCurrentEdit();

      if (percentCompleteThreshold != ui.value) {
        window.clearTimeout(h_runfilters);
        h_runfilters = window.setTimeout(updateFilter, 10);
        percentCompleteThreshold = ui.value;
      }
    }
  });


  // wire up the search textbox to apply the filter to the model
  $("#txtSearch,#txtSearch2").keyup(function (e) {
    Slick.GlobalEditorLock.cancelCurrentEdit();

    // clear on Esc
    if (e.which == 27) {
      this.value = "";
    }

    searchString = this.value;
    updateFilter();
  });

  function updateFilter() {
    dataView.setFilterArgs({
      percentCompleteThreshold: percentCompleteThreshold,
      searchString: searchString
    });
    dataView.refresh();
  }

  $("#btnSelectRows").click(function () {
    if (!Slick.GlobalEditorLock.commitCurrentEdit()) {
      return;
    }

    var rows = [];
    for (var i = 0; i < 10 && i < dataView.getLength(); i++) {
      rows.push(i);
    }

    grid.setSelectedRows(rows);
  });


  // initialize the model after all the events have been hooked up
  dataView.beginUpdate();
  dataView.setItems(data);
  dataView.setFilterArgs({
    percentCompleteThreshold: percentCompleteThreshold,
    searchString: searchString
  });
  dataView.setFilter(myFilter);
  dataView.endUpdate();

  // if you don't want the items that are not visible (due to being filtered out
  // or being on a different page) to stay selected, pass 'false' to the second arg
  //dataView.syncGridSelection(grid, false);

  $("#gridContainer").resizable();
})
