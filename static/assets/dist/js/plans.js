// variable para gestionar los elementos seleccionados
let selected_id;

// Variable con el token
const csrfToken = document.cookie
  .split(";")
  .find((c) => c.trim().startsWith("csrftoken="))
  ?.split("=")[1];
// url del endpoint principal
const url = "/product-gestion/plan/";

$(document).ready(function () {
  // var texto = prompt('Entra algo:');
  // test();
  $("table")
    .addClass("table table-hover")
    .DataTable({
      responsive: true,
      dom: '<"top"l>Bfrtip',
      buttons: [
        {
          text: " Agregar",
          className: " btn btn-primary btn-info",
          action: function (e, dt, node, config) {
            $("#modal-crear-elemento").modal("show");
          },
        },
        {
          extend: "excel",
          text: "Excel",
        },
        {
          extend: "pdf",
          text: "PDF",
        },
        {
          extend: "print",
          text: "Imprimir",
        },
      ],
      //Adding server-side processing
      serverSide: true,
      search: {
        return: true,
      },
      processing: true,
      ajax: function (data, callback, settings) {
        dir = "";
        if (data.order[0].dir == "desc") {
          dir = "-";
        }
        console.log(data.length);
        axios
          .get(url, {
            params: {
              page_size: data.length,
              page: data.start / data.length + 1,
              search: data.search.value,
              ordering: dir + data.columns[data.order[0].column].data,
            },
          })
          .then((res) => {
            callback({
              recordsTotal: res.data.count,
              recordsFiltered: res.data.count,
              data: res.data.results,
            });
          })
          .catch((error) => {
            alert(error);
          });
        console.log(data);
      },
      columns: [
        { data: "name", title: "Nombre" },
        { data: "ueb.name", title: "UEB" },
        { data: "destiny.name", title: "Destino" },
        { data: "product_kind.name", title: "Tipo de producto" },
        { data: "year", title: "Año" },
        { data: "month", title: "Mes" },
        { data: "quantity", title: "Cantidad" },
        { data: "measurement_unit.name", title: "Unidad de medida" },
        {
          data: null,
          title: "Acciones",
          render: (data, type, row) => {
            return `<div class="btn-group">
                        <button type="button" title="edit" class="btn bg-olive active" data-toggle="modal" data-target="#modal-crear-elemento" data-id="${row.id}" data-type="edit" data-name="${row.name}" id="${row.id}"  >
                          <i class="fas fa-edit"></i></button>                       
                        <button type="button" title="delete" class="btn bg-olive" data-toggle="modal" data-target="#modal-eliminar-elemento" data-id="${row.id}" data-name="${row.name}" id="${row.id}">
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>`;
          },
        },
      ],
      //  esto es para truncar el texto de las celdas
      columnDefs: [
        {
          targets: 0,
          render: function (data, type, row) {
            if (data == null || data == "") {
              return (data = "Sin Datos");
            } else {
              return type === "display" && data.length > 20
                ? data.substr(0, 20) + "…"
                : data;
            }
          },
        },
        {
          targets: 1,
          render: function (data, type, row) {
            if (data == null || data == "") {
              return (data = "Sin Datos");
            } else {
              return type === "display" && data.length > 20
                ? data.substr(0, 20) + "…"
                : data;
            }
          },
        },
      ],
    });
});

$("#modal-eliminar-elemento").on("show.bs.modal", function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
  var dataName = button.data("name"); // Extract info from data-* attributes
  selected_id = button.data("id"); // Extract info from data-* attributes
  var modal = $(this);
  modal.find(".modal-body").text("¿Desea eliminar el plan: " + dataName + "?");
});

// funcion para eliminar usuario
function function_delete(selected_id) {
  const table = $("#tabla-de-Datos").DataTable();
  axios.defaults.headers.common["X-CSRFToken"] = csrfToken;
  axios
    .delete(`${url}${selected_id}/`)
    .then((response) => {
      Toast.fire({
        icon: "success",
        title: "El plan se eliminó correctamente",
      });
      table.row(`#${selected_id}`).remove().draw(); // use id selector to remove the row
    })
    .catch((error) => {
      Toast.fire({
        icon: "error",
        title: "El plan no se eliminó",
      });
    });
}

// reinicia y limpia el formulario despues de editar
$("#modal-crear-elemento").on("hide.bs.modal", (event) => {
  // The form element is selected from the event trigger and its value is reset.
  const form = event.currentTarget.querySelector("form");
  form.reset();
  // The 'edit_elemento' flag is set to false.
  edit_elemento = false;
  // An array 'elements' is created containing all the HTML elements found inside the form element.
  const elements = [...form.elements];
  // A forEach loop is used to iterate through each element in the array.
  elements.forEach((elem) => elem.classList.remove("is-invalid"));
});

// carga los datos para editar
let edit_elemento = false;
$("#modal-crear-elemento").on("show.bs.modal", function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
  var modal = $(this);
  if (button.data("type") == "edit") {
    var dataName = button.data("name"); // Extract info from data-* attributes
    selected_id = button.data("id"); // Extract info from data-* attributes
    edit_elemento = true;
    modal.find(".modal-title").text("Editar " + dataName);
    // Realizar la petición con Axios
    axios
      .get(`${url}${selected_id}/`)
      .then(function (response) {
        // Recibir la respuesta
        const element = response.data;
        // Llenar el formulario con los datos del usuario
        form.elements.name.value = element.name;
        $("#ueb").val(element.ueb.id).trigger("change.select2");
        $("#destiny").val(element.destiny.id).trigger("change.select2");
        $("#classification")
          .val(element.product_kind.id)
          .trigger("change.select2");
        form.elements.quantity.value = element.quantity;
        $("#measurement_unit")
          .val(element.measurement_unit.id)
          .trigger("change.select2");
        form.elements.date.value = element.month + "-" + element.year;
        console.log("ver");
        console.log(element.quantity);
      })
      .catch(function (error) {});
  } else {
    modal.find(".modal-title").text("Crear Plan");
  }
});

$(function () {
  $(".select2").select2({
    dropdownParent: $("#modal-crear-elemento"),
    theme: "bootstrap4",
  });
  bsCustomFileInput.init();
  poblarListas();
});

// form validator
$(function () {
  $.validator.setDefaults({
    language: "es",
    submitHandler: function () {
      // alert("Form successful submitted!");
    },
  });
  $("#form-create-elemento").validate({
    rules: {
      name: {
        required: true,
      },
      ueb: {
        required: true,
      },
      destiny: {
        required: true,
      },

      product: {
        required: true,
      },
      date: {
        required: true,
        dateFormat: true,
      },

      quantity: {
        required: true,
        digits: true,
        min: 1,
      },
      measurement_unit: {
        required: true,
      },
    },
    submitHandler: function (form) {},

    messages: {
      name: {
        required: "El nombre del plan es obligatorio",
      },
      date: {
        required: "El plan debe responder a una fecha",
      },
      quantity: {
        required: "Por favor, ingresa la cantidad planificada.",
        digits: "Por favor, ingresa solo números enteros positivos.",
        min: "La capacidad debe ser un número positivo.",
      },
    },
    errorElement: "span",
    errorPlacement: function (error, element) {
      error.addClass("invalid-feedback");
      element.closest(".form-group").append(error);
    },
    highlight: function (element, errorClass, validClass) {
      $(element).addClass("is-invalid");
    },
    unhighlight: function (element, errorClass, validClass) {
      $(element).removeClass("is-invalid");
    },
  });
});

// crear elementos

let form = document.getElementById("form-create-elemento");
form.addEventListener("submit", function (event) {
  event.preventDefault();
  var table = $("#tabla-de-Datos").DataTable();
  axios.defaults.headers.common["X-CSRFToken"] = csrfToken;
  if (form.checkValidity()) {
    let data = new FormData();
    data.append("name", document.getElementById("name").value);
    data.append("destiny", document.getElementById("destiny").value);
    data.append(
      "product_kind",
      document.getElementById("classification").value
    );
    data.append("ueb", document.getElementById("entity").value);
    data.append("quantity", document.getElementById("quantity").value);
    data.append(
      "measurement_unit",
      document.getElementById("measurement_unit").value
    );
    var date = document.getElementById("date").value;
    var parts = date.split("-");
    console.log(convertMonthToNumber(parts[0]));
    data.append("month", convertMonthToNumber(parts[0]));
    data.append("year", parts[1]);
    if (edit_elemento) {
      axios
        .put(`${url}${selected_id}/`, data)
        .then((response) => {
          if (response.status === 200) {
            Swal.fire({
              icon: "success",
              title: "Plan editado con éxito",
              showConfirmButton: false,
              timer: 1500,
            });

            table.ajax.reload();
            $("#modal-crear-elemento").modal("hide");
            edit_elemento = false;
          }
        })
        .catch((error) => {
          let dict = error.response.data;
          console.log(dict);
          let textError = "Revise los siguientes campos: ";
          for (const key in dict) {
            console.log(key);
            textError = textError + ", " + key + ": " + dict[key][0] + " ";
            $("#" + key).addClass("is-invalid");
            if (key === "month" || key === "year") {
              $("#date").addClass("is-invalid");
            }
          }

          Swal.fire({
            icon: "error",
            title: "Error al crear plan",
            text: textError,
            showConfirmButton: false,
            timer: 3000,
          });
        });
    } else {
      axios
        .post(url, data)
        .then((response) => {
          if (response.status === 201) {
            Swal.fire({
              icon: "success",
              title: "Plan creado con éxito",
              showConfirmButton: false,
              timer: 3000,
            });

            table.ajax.reload();
            $("#modal-crear-elemento").modal("hide");
          }
        })
        .catch((error) => {
          let dict = error.response.data;
          let textError = "Revise los siguientes campos: ";
          for (const key in dict) {
            textError = textError + ", " + key + ": " + dict[key];
          }

          Swal.fire({
            icon: "error",
            title: "Error al crear plan",
            text: textError,
            showConfirmButton: true,
            timer: 50 * textError.length,
          });
        });
    }
  }
});

function poblarListas() {
  var $destiny = document.getElementById("destiny");
  axios.get("/product-gestion/destination/").then(function (response) {
    response.data.results.forEach(function (element) {
      var option = new Option(element.name, element.id);
      $destiny.add(option);
    });
  });

  var $classification = document.getElementById("classification");
  axios.get("/product-gestion/classification/").then(function (response) {
    response.data.results.forEach(function (element) {
      var option = new Option(element.name, element.id);
      $classification.add(option);
    });
  });

  var $measurement_unit = document.getElementById("measurement_unit");
  axios
    .get("/product-gestion/measurement-unit/?used_for_planning=true")
    .then(function (response) {
      response.data.results.forEach(function (element) {
        var option = new Option(element.name, element.id);
        $measurement_unit.add(option);
      });
    });
  var $entity = document.getElementById("entity");
  axios.get("/product-gestion/entity/").then(function (response) {
    response.data.results.forEach(function (element) {
      var option = new Option(element.name, element.id);
      $entity.add(option);
    });
  });
}

function convertMonthToNumber(month) {
  // Si el mes es un número, lo devolvemos.
  const processedMonth = validateNumber(month);
  if (processedMonth) {
    return processedMonth;
  }

  // Si el mes es una cadena, lo convertimos a número.
  const months = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
  ];
  const monthNumber = months.indexOf(month.toLowerCase());

  // Si el mes no es válido, devolvemos -1.
  if (monthNumber === -1) {
    return -1;
  }
  console.log(monthNumber + 1);
  return monthNumber + 1;
}

function validateNumber(number) {
  // Si el número es una cadena, lo convertimos a número.
  const numberAsNumber = parseInt(number, 10);

  // Comprobamos que el número sea un número.
  if (isNaN(numberAsNumber) || numberAsNumber < 1 || numberAsNumber > 11) {
    return false;
  }
  // El número es válido.
  return numberAsNumber;
}
