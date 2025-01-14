// variable para gestionar los elementos seleccionados
let selected_id;

// Variable con el token
const csrfToken = document.cookie
  .split(";")
  .find((c) => c.trim().startsWith("csrftoken="))
  ?.split("=")[1];
// url del endpoint principal
const url = "/product-gestion/classification/";
// url del endpoint principal con el filtro de parent
const urlfilter = "/product-gestion/classification/?parent__isnull=false";

$(document).ready(function () {
  // var texto = prompt('Entra algo:');
  test();
  $("table")
    .addClass("table table-hover")
    .DataTable({
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
          .get(urlfilter, {
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
        // { data: "parent", "title": "Padre" },
        { data: "description", title: "Descripción" },
        {
          data: "",
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
          targets: 1,
          render: function (data, type, row) {
            if (data == null || data == "") {
              return (data = " ");
            } else {
              return type === "display" && data.length > 80
                ? data.substr(0, 80) + "…"
                : data;
            }
          },
        },
      ],
    });
  poblarListas();
});

$("#modal-eliminar-elemento").on("show.bs.modal", function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
  var dataName = button.data("name"); // Extract info from data-* attributes
  selected_id = button.data("id"); // Extract info from data-* attributes
  var modal = $(this);
  modal
    .find(".modal-body")
    .text("¿Desea eliminar la clasificación: " + dataName + "?");
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
        title: "La clasificación seleccionada se eliminó correctamente",
      });
      table.row(`#${selected_id}`).remove().draw(); // use id selector to remove the row
    })
    .catch((error) => {
      Toast.fire({
        icon: "error",
        title: "La clasificación seleccionada no se eliminó",
      });
    });
}

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
  poblarListas();
});

var datar = {
  id: 1,
  text: "Barn owl",
};
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
        const elemento = response.data;

        // Llenar el formulario con los datos del usuario
        $("#parent").select2({
          dropdownParent: $("#modal-crear-elemento"),
          theme: "bootstrap4",
        });
        $("#parent").val(elemento.parent).trigger("change.select2");
        form.elements.name.value = elemento.name;
        form.elements.description.value = elemento.description;
      })
      .catch(function (error) {});
  } else {
    modal.find(".modal-title").text("Crear nueva clasificación");
  }
});

$(function () {
  $(".select2").select2({
    dropdownParent: $("#modal-crear-elemento"),
    theme: "bootstrap4",
  });

  bsCustomFileInput.init();
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
    },
    submitHandler: function (form) {},

    messages: {
      name: {
        required: "Por favor debe proporcionar un nombre",
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

// crear usuario
let form = document.getElementById("form-create-elemento");
form.addEventListener("submit", function (event) {
  event.preventDefault();
  var table = $("#tabla-de-Datos").DataTable();
  axios.defaults.headers.common["X-CSRFToken"] = csrfToken;
  if (form.checkValidity()) {
    let data = new FormData();
    data.append("parent", document.getElementById("parent").value);
    data.append("name", document.getElementById("name").value);
    data.append("description", document.getElementById("description").value);

    if (edit_elemento) {
      axios
        .put(`${url}${selected_id}/`, data)
        .then((response) => {
          if (response.status === 200) {
            Swal.fire({
              icon: "success",
              title: "Clasificación actualizada con éxito",
              showConfirmButton: false,
              timer: 50 * textError.length,
            });

            table.ajax.reload();
            $("#modal-crear-elemento").modal("hide");
            edit_elemento = false;
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
            title: "Error al crear clasificación",
            text: textError,
            showConfirmButton: false,
            timer: 50 * textError.length,
          });
        });
    } else {
      axios
        .post(url, data)
        .then((response) => {
          if (response.status === 201) {
            Swal.fire({
              icon: "success",
              title: "Clasificación creada con éxito",
              showConfirmButton: false,
              timer: 50 * textError.length,
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
            title: "Error al crear clasificación",
            text: textError,
            showConfirmButton: false,
            timer: 50 * textError.length,
          });
        });
    }
  }
});

function test() {
  axios.get(url).then(function (response) {
    console.log(response.data.results);
  });
}

function poblarListas() {
  var $classification = document.getElementById("parent");
  $classification.innerHTML = "";
  axios.get("/product-gestion/classification/").then(function (response) {
    response.data.results.forEach(function (element) {
      var option = new Option(element.name, element.id);
      $classification.add(option);
    });
  });
}
