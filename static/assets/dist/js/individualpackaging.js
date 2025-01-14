// variable para gestionar los elementos seleccionados
let selected_id;

// Variable con el token
const csrfToken = document.cookie
  .split(";")
  .find((c) => c.trim().startsWith("csrftoken="))
  ?.split("=")[1];
// url del endpoint principal
const url = "/product-gestion/individual-packaging/";
const url_filter = "/product-gestion/individual-packaging/?is_active=true";

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
          .get(url_filter, {
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
        { data: "name_representation", title: "Nombre" },
        { data: "capacity", title: "Capacidad" },
        { data: "description", title: "Descripción" },
        { data: "measurement_unit.name", title: "U/M" },
        {
          data: "",
          title: "Empaque",
          className: "text-center",
          render: (data, type, row) => {
            if (row.is_grouping_packaging) {
              return `<i class="nav-icon fas fa-cubes"></i>`;
            } else {
              return `<i class="nav-icon fas fa-cube"></i>`;
            }
          },
        },
        {
          data: "",
          title: "Acciones",
          className: "text-center",
          render: (data, type, row) => {
            if (row.deletion_timestamp == null) {
              return `<div class="btn-group">
    <button type="button" title="edit" class="btn bg-olive active" data-toggle="modal" data-target="#modal-crear-elemento" data-id="${row.id}" data-type="edit" data-name="${row.name}" id="${row.id}"  >
      <i class="fas fa-edit"></i></button>   
                       
    <button type="button" title="Agrupador" class="btn bg-olive " data-toggle="modal" data-target="#modal-crear-agrupador" data-id="${row.id}" data-type="grouping" data-name="${row.name}" id="${row.id}"  >
      <i class="fas fa-cubes"></i></button>                       
    
    <button type="button" title="Archivar" class="btn bg-teal" data-toggle="modal" data-target="#modal-eliminar-elemento" data-id="${row.id}" data-name="${row.name}" id="${row.id}">
      <i class="fas fa-archive"></i>
    </button>
  </div>`;
            } else {
              return `<div class="btn-group">
    <button type="button" title="edit" class="btn bg-olive active" data-toggle="modal" data-target="#modal-crear-elemento" data-id="${row.id}" data-type="edit" data-name="${row.name}" id="${row.id}"  >
      <i class="fas fa-edit"></i></button>   
                       
    <button type="button" title="Agrupador" class="btn bg-olive " data-toggle="modal" data-target="#modal-crear-agrupador" data-id="${row.id}" data-type="grouping" data-name="${row.name}" id="${row.id}"  >
      <i class="fas fa-cubes"></i></button>                       
    
    <button type="button" title="Restaurar" class="btn bg-teal" data-toggle="modal" data-id="${row.id}" data-name="${row.name}" id="${row.id}" onclick="function_des_archivar(${row.id})">
      <i class="fas fa-box-open"></i>
    </button>
  </div>`;
            }
          },
        },
      ],
      //  esto es para truncar el texto de las celdas
      columnDefs: [
        {
          targets: 2,
          render: function (data, type, row) {
            if (data == null || data == "") {
              return (data = "Sin Datos");
            } else {
              return type === "display" && data.length > 50
                ? data.substr(0, 50) + "…"
                : data;
            }
          },
        },
      ],
    });
  poblarListas();
});

$("#modal-eliminar-elemento").on("hide.bs.modal", (event) => {
  document.getElementById("cause").value = "";
});

$("#modal-eliminar-elemento").on("show.bs.modal", function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
  var dataName = button.data("name"); // Extract info from data-* attributes
  selected_id = button.data("id"); // Extract info from data-* attributes
  var modal = $(this);
  modal
    .find(".mytext")
    .text("¿Desea archivar el tipo de envase: " + dataName + "?");
});

// funcion para archivar
function function_archivar(selected_id) {
  const table = $("#tabla-de-Datos").DataTable();
  axios.defaults.headers.common["X-CSRFToken"] = csrfToken;
  let data = new FormData();
  data.append("deletion_cause", document.getElementById("cause").value);
  axios
    .post(`${url}${selected_id}/archive/`, data)
    .then((response) => {
      Toast.fire({
        icon: "success",
        title: "El tipo de envase se archivó correctamente",
      });
      table.ajax.reload();
    })
    .catch((error) => {
      Toast.fire({
        icon: "error",
        title: "El tipo de envase no se archivó",
      });
    });
}
// funcion para des archivar
function function_des_archivar(selected_id) {
  const table = $("#tabla-de-Datos").DataTable();
  axios.defaults.headers.common["X-CSRFToken"] = csrfToken;
  let data = new FormData();
  data.append("deletion_cause", document.getElementById("cause").value);
  axios
    .post(`${url}${selected_id}/des_archive/`, data)
    .then((response) => {
      Toast.fire({
        icon: "success",
        title: "El tipo de envase se restauró correctamente",
      });
      table.ajax.reload();
    })
    .catch((error) => {
      Toast.fire({
        icon: "error",
        title: "El tipo de envase no se restauró",
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
});

let edit_elemento = false;
$("#modal-crear-elemento").on("show.bs.modal", function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
  var modal = $(this);
  // poblarListas();
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
        console.log("✌️elemento --->", elemento.measurement_unit);
        // console.log(elemento);
        //
        // Llenar el formulario con los datos del usuario
        form.elements.name.value = elemento.name;
        form.elements.capacity.value = elemento.capacity;
        form.elements.munit.value = elemento.measurement_unit.id;
        form.elements.description.value = elemento.description;
        form.elements.is_grouping_packaging.value =
          elemento.is_grouping_packaging;
        if (elemento.is_grouping_packaging) {
          form.elements.is_grouping_packaging.checked = true;
        }
      })
      .catch(function (error) {});
  } else {
    modal.find(".modal-title").text("Crear tipo de envase");
  }
});

$(function () {
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
      capacity: {
        required: true,
        digits: true,
        min: 1,
      },
    },
    submitHandler: function (form) {},

    messages: {
      capacity: {
        required: "Por favor, ingresa la capacidad.",
        digits: "Por favor, ingresa solo números enteros positivos.",
        min: "La capacidad debe ser un número positivo.",
      },
      name: {
        required: "El nombre es requerido.",
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
  // Validar el formulario
  if (form.checkValidity()) {
    let data = new FormData();
    data.append("name", document.getElementById("name").value);
    data.append("capacity", document.getElementById("capacity").value);
    data.append("measurement_unit", document.getElementById("munit").value);
    data.append("description", document.getElementById("description").value);
    if (document.getElementById("is_grouping_packaging").checked) {
      data.append("is_grouping_packaging", true);
    } else {
      data.append("is_grouping_packaging", false);
    }
    // data.append("is_grouping_packaging", document.getElementById("is_grouping_packaging").value);

    if (edit_elemento) {
      axios
        .put(`${url}${selected_id}/`, data)
        .then((response) => {
          if (response.status === 200) {
            Swal.fire({
              icon: "success",
              title: "Tipo de envase editado con éxito",
              showConfirmButton: false,
              timer: 2000,
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
            title: "Error al crear Tipo de envase ",
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
              title: "Tipo de envase creado con éxito",
              showConfirmButton: false,
              timer: 2000,
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
            title: "Error al crear elemento",
            text: textError,
            showConfirmButton: false,
            timer: 50 * textError.length,
          });
        });
    }
  }
});

// -------------------------------------------------------------------------------------------------------

// ------------------------------------modal-crear-agrupador------------------------------------------------------
$("#modal-crear-agrupador").on("hide.bs.modal", (event) => {
  // The form element is selected from the event trigger and its value is reset.
  const form = event.currentTarget.querySelector("form");
  form.reset();
  // An array 'elements' is created containing all the HTML elements found inside the form element.
  const elements = [...form.elements];
  // A forEach loop is used to iterate through each element in the array.
  elements.forEach((elem) => elem.classList.remove("is-invalid"));
});

var selected_id_ag;
// let edit_elemento = false;
$("#modal-crear-agrupador").on("show.bs.modal", function (event) {
  var button = $(event.relatedTarget);
  selected_id_ag = button.data("id");
});

let formagrupador = document.getElementById("form-crear-agrupador");

formagrupador.addEventListener("submit", function (event) {
  event.preventDefault();
  var table = $("#tabla-de-Datos").DataTable();
  axios.defaults.headers.common["X-CSRFToken"] = csrfToken;
  let data = new FormData();
  data.append("name", document.getElementById("nameag").value);
  data.append("capacity", document.getElementById("capacityag").value);
  data.append("individual_packaging", selected_id_ag);
  data.append("description", document.getElementById("descriptionag").value);
  const url2 = "/product-gestion/grouping-packaging/";
  axios
    .post(url2, data)
    .then((response) => {
      if (response.status === 201) {
        Swal.fire({
          icon: "success",
          title: "Envase agrupador creado con éxito",
          showConfirmButton: false,
          timer: 2000,
        });

        // table.ajax.reload();
        $("#modal-crear-agrupador").modal("hide");
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
        title: "Error al crear elemento",
        text: textError,
        showConfirmButton: false,
        timer: 50 * textError.length,
      });
    });
});

function test() {
  axios.get(url).then(function (response) {
    console.log(response.data.results);
  });
}

function poblarListas() {
  var $responsability = document.getElementById("munit");
  axios.get("/product-gestion/measurement-unit/").then(function (response) {
    response.data.results.forEach(function (element) {
      var option = new Option(element.name, element.id);
      $responsability.add(option);
    });
  });
}

function changeCheckboxValue(id) {
  // Get the checkbox element by ID
  const checkboxElement = document.getElementById(id);

  if (checkboxElement.checked) {
    // If the checkbox is already checked, set its value to true
    checkboxElement.value = true;
  } else {
    // Otherwise, set its value to false
    checkboxElement.value = false;
  }
}
