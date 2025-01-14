let credencial;
let checkcredencial;

$(document).ready(function () {
  $("table")
    .addClass("table table-hover")
    .DataTable({
      dom: '<"top"l>Bfrtip',
      buttons: [
        {
          text: " Agregar",
          className: " btn btn-primary btn-info",
          action: function (e, dt, node, config) {
            $("#modal-crear-usuario").modal("show");
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

        axios
          .get("/user-gestion/users/", {
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
      },
      columns: [
        {
          data: "photo",
          title: "Foto",
          render: (data) => {
            if (data) {
              return `<div class="text-center" ><img class="profile-user-img img-fluid img-circle" src="${data}"></div>`;
            } else {
              return `<div class="text-center" ><img class="profile-user-img img-fluid img-circle" src="/static/assets/dist/img/user8-128x128.jpg"></div>`;
            }
          },
        },
        { data: "username", title: "Usuario" },
        { data: "get_full_name", title: "Nombre y Apellidos" },
        { data: "ci", title: "CI" },
        { data: "gender", title: "Género" },
        {
          data: "",
          title: "Acciones",
          render: (data, type, row) => {
            return `<div class="btn-group">
                        <button type="button" title="edit" class="btn bg-olive active" data-toggle="modal" data-target="#modal-crear-usuario" data-id="${row.id}" data-type="edit" data-name="${row.get_full_name}" id="${row.id}"  >
                          <i class="fas fa-edit"></i>
                        </button>                       
                        <button type="button" title="delete" class="btn bg-olive" data-toggle="modal" data-target="#modal-eliminar-usuario" data-id="${row.id}" data-name="${row.get_full_name}" id="${row.id}">
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>`;
          },
        },
      ],
      //  esto es para truncar el texto de las celdas
      columnDefs: [],
    });
  // aqui se llama la funcion para poblar las listas del formulario
  poblarListas();
  credencial = document.getElementById("credencial");
  checkcredencial = document.getElementById("checkcredencial");
  checkcredencial.addEventListener("change", () => {
    // Si el checkbox está marcado, habilitar los inputs, de lo contrario, deshabilitarlos
    if (checkcredencial.checked) {
      document.getElementById("password").disabled = false;
      document.getElementById("inputPasswordValidate").disabled = false;
    } else {
      document.getElementById("password").disabled = true;
      document.getElementById("inputPasswordValidate").disabled = true;
    }
  });
});

let selected_id;

$("#modal-eliminar-usuario").on("show.bs.modal", function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
  var dataName = button.data("name"); // Extract info from data-* attributes
  var dataId = button.data("id"); // Extract info from data-* attributes
  selected_id = button.data("id"); // Extract info from data-* attributes
  var modal = $(this);
  modal
    .find(".modal-body")
    .text("¿Desea eliminar al usuario " + dataName + "?");
});

// funcion para eliminar usuario
function function_delete(selected_id) {
  const table = $("#tabla-de-Datos").DataTable();
  const csrfToken = document.cookie
    .split(";")
    .find((c) => c.trim().startsWith("csrftoken="))
    ?.split("=")[1];
  axios.defaults.headers.common["X-CSRFToken"] = csrfToken;
  axios
    .delete(`/user-gestion/users/${selected_id}/`)
    .then((response) => {
      Toast.fire({
        icon: "success",
        title: "El usuario se eliminó correctamente",
      });
      table.row(`#${selected_id}`).remove().draw(); // use id selector to remove the row
    })
    .catch((error) => {
      Toast.fire({
        icon: "error",
        title: "El usuario no se eliminó",
      });
    });
}

$("#modal-crear-usuario").on("hide.bs.modal", (event) => {
  // The form element is selected from the event trigger and its value is reset.
  const form = event.currentTarget.querySelector("form");
  form.reset();
  // The 'edit_user' flag is set to false.
  edit_user = false;
  // An array 'elements' is created containing all the HTML elements found inside the form element.
  const elements = [...form.elements];
  // A forEach loop is used to iterate through each element in the array.
  elements.forEach((elem) => elem.classList.remove("is-invalid"));
});

let edit_user = false;
$("#modal-crear-usuario").on("show.bs.modal", function (event) {
  console.log(credencial);
  document.getElementById("password").disabled = false; //para deshabilitar los input de password
  document.getElementById("inputPasswordValidate").disabled = false;

  var button = $(event.relatedTarget); // Button that triggered the modal
  var modal = $(this);
  if (button.data("type") == "edit") {
    var dataName = button.data("name"); // Extract info from data-* attributes
    var dataId = button.data("id"); // Extract info from data-* attributes
    selected_id = button.data("id"); // Extract info from data-* attributes
    edit_user = true;
    credencial.style.display = "block";
    // document.getElementById("username").disabled = true;//para deshabilitar los input de password
    document.getElementById("password").disabled = true; //para deshabilitar los input de password
    document.getElementById("inputPasswordValidate").disabled = true;
    modal.find(".modal-title").text("Editar al usuario " + dataName);
    // Definir la URL
    const url = "/user-gestion/users/" + selected_id + "/";
    // Realizar la petición con Axios
    axios
      .get(url)
      .then(function (response) {
        // Recibir la respuesta
        const user = response.data;
        console.log(user);
        // Llenar el formulario con los datos del usuario
        form.elements.username.value = user.username;
        form.elements.email.value = user.email;
        form.elements.first_name.value = user.first_name;
        form.elements.last_name.value = user.last_name;
        form.elements.ci.value = user.ci;
        form.elements.gender.value = user.gender;
        form.elements.area.value = user.area;
        form.elements.responsability.value = user.responsability;
      })
      .catch(function (error) {});
  } else {
    modal.find(".modal-title").text("Crear usuario");
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

  $("#form-create-user").validate({
    rules: {
      first_name: {
        required: true,
      },
      last_name: {
        required: true,
      },
      ci: {
        required: true,
      },
      email: {
        required: true,
        email: true,
      },
      username: {
        required: true,
      },
      password: {
        required: true,
        minlength: 5,
      },
      inputPasswordValidate: {
        required: true,
        minlength: 5,
        equalTo: "#password",
      },
    },
    submitHandler: function (form) {},

    messages: {
      email: {
        required: "Por favor debe ingresar una dirección de correo",
        email: "Por favor debe ingresar una dirección de correo válida",
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
let form = document.getElementById("form-create-user");
form.addEventListener("submit", function (event) {
  event.preventDefault();
  var table = $("#tabla-de-Datos").DataTable();
  const csrfToken = document.cookie
    .split(";")
    .find((c) => c.trim().startsWith("csrftoken="))
    ?.split("=")[1];
  axios.defaults.headers.common["X-CSRFToken"] = csrfToken;
  let data = new FormData();

  data.append("username", document.getElementById("username").value);
  data.append("email", document.getElementById("email").value);
  data.append("first_name", document.getElementById("first_name").value);
  data.append("last_name", document.getElementById("last_name").value);
  data.append("is_staff", true);
  data.append("ci", document.getElementById("ci").value);
  data.append("gender", document.getElementById("gender").value);
  data.append("area", document.getElementById("area").value);
  data.append(
    "responsability",
    document.getElementById("responsability").value
  );

  if (
    document.getElementById("password").value != "" &&
    document.getElementById("inputPasswordValidate").value != "" &&
    document.getElementById("password").value ===
      document.getElementById("inputPasswordValidate").value
  ) {
    data.append("password", document.getElementById("password").value);
  } else {
    if (
      (checkcredencial.checked &&
        document.getElementById("password").value == "") ||
      document.getElementById("password").value !=
        document.getElementById("inputPasswordValidate").value
    ) {
      // alert("se jidio");
      event.preventDefault();
      return;
    }
  }

  if (document.getElementById("customFile").files[0] != null) {
    data.append("photo", document.getElementById("customFile").files[0]);
  }

  const url = "/user-gestion/users/";
  let rowNode;
  if (edit_user) {
    axios
      .patch(url + selected_id + "/", data)
      .then((response) => {
        if (response.status === 200) {
          $("#modal-crear-usuario").modal("hide");
          Swal.fire({
            icon: "success",
            title: "Usuario actualizado con exito  ",
            showConfirmButton: false,
            timer: 50 * textError.length,
          });
          table.ajax.reload();

          edit_user = false;
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
          title: "Error al crear usuario",
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
            title: "Usuario creado con exito",
            showConfirmButton: false,
            timer: 50 * textError.length,
          });
          table.ajax.reload();
          $("#modal-crear-usuario").modal("hide");
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
          title: "Error al crear usuario",
          text: textError,
          showConfirmButton: false,
          timer: 50 * textError.length,
        });
      });
  }
});

// aquí se cargan los datos para responsability y area desde sus endpoint

function poblarListas() {
  var $responsability = document.getElementById("responsability");
  axios
    .get("..//user-gestion/employee-responsability/")
    .then(function (response) {
      response.data.results.forEach(function (element) {
        var option = new Option(element.name, element.id);
        $responsability.add(option);
      });
    });
  var $area = document.getElementById("area");
  axios.get("..//user-gestion/employee-area/").then(function (response) {
    response.data.results.forEach(function (element) {
      var option = new Option(element.name, element.id);
      $area.add(option);
    });
  });
}
