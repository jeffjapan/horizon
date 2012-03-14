horizon.addInitFunction(function() {
  $('.table_search input').quicksearch('tbody tr', {
    'delay': 300,
    'loader': 'span.loading',
    'bind': 'keyup click',
    'show': function () {
      this.style.display = '';
    },
    'hide': function () {
      this.style.display = 'none';
    },
    'prepareQuery': function (val) {
      return new RegExp(val, "i");
    },
    'testQuery': function (query, txt, _row) {
      return query.test($(_row).find('td:not(.hidden)').text());
    }
  });

  $('table.sortable').each(function(index, table) {
      var $table = $(table);
      // Only trigger if we have actual data rows in the table.
      // Calling on an empty table throws a javascript error.
      if ($table.find('tbody tr').length) {
        $table.tablesorter();
      }
    });

  horizon.datatables.update();
});
