$(document).ready(function () {
  if ($.fn.DataTable.isDataTable("#miTabla")) {
    $("#miTabla").DataTable().clear().destroy();
  }

  $("#miTabla").DataTable({
    paging: false,
    info: false,
    ordering: true,
    searching: true,
    columnDefs: [{ targets: -1, orderable: false }],
    language: {
      zeroRecords: "No se encontraron registros",
      searchPlaceholder: "Buscar...",
      search: '',
    },
  });

  $("#miTabla_filter")
    .removeClass("dataTables_filter")
    .addClass("d-grid gap-2 d-md-flex justify-content-md-end pb-2");
  $("#miTabla_filter input")
    .unwrap()
    .wrap('<div class="col-md-3"></div>')
    .addClass("form-control form-control");
});

var tooltipTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="tooltip"]')
);
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl);
});
