var searchMaster = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('q'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: '/product_list?q=%QUERY',
    remote: {
      url: '/search_master_typeahead?q=%QUERY',
      wildcard: '%QUERY'
    }
  });
  $('#search_form .typeahead').typeahead({
    //hint:true,
    //highlight: true,
    //autoselect: true,
    minLength:2,
    limit: 10,
  }, {
    name: 'searchMaster',
    displayKey: 'q',
    source: searchMaster,
    templates:{
      empty: 'Не має в базі',
    }
  });
  $('#search_form').submit(function(e) {
    $.get('/product_list_by_master', $(this).serialize(), function(data) {
        $('#product_list').html(data.html_form);
    });
    e.preventDefault();
  });
  