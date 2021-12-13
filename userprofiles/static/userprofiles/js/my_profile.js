    /* --- Start Info Modal --- */

$(document).ready(function () {
    $(".modal").modal();
    $("#modal1").modal("open");
});

/*
const toFollowModalBody = document.getElementById('to-follow-modal')
const spinnerBox = document.getElementById('spinner-box')
const toFollowBtn = document.getElementById('to-follow-btn')
let toFollowLoad = false


console.log(toFollowModalBody)
console.log(spinnerBox)

// -- To follow button -- //

toFollowBtn.addEventListener('click', () => {
    $.ajax({
        type: 'GET',
        url: '/profileusers/profile_data/',
        success: function (response) {
            if (!toFollowLoad) {
                console.log(response);
                const pfData = response.pf_data;
                console.log(pfData);
                setTimeout(() => {
                    spinnerBox.classList.add('not-visible');
                    pfData.forEach(el => {
                        toFollowModalBody.innerHTML += `
                        <div class="row mb-2">
                            <div class="col-3 text-center">
                                <img class="avatar" src="${el.avatar}" alt="${el.user}">
  
                            </div>
                            <div class="col-4 text-center">
                                
                                <div class="text-muted"><strong>${el.firstname}</strong></div>
                                <div class="text-muted"><strong>${el.lastname}</strong></div>
                            </div>
                            <div class="col-5 text-center">
                                <div class="text-muted">${el.profession}</div>
                                <div class="text-muted">${el.company_name}</div>
                            </div>
                        </div>
                        <div class="row mb-2">
                            <div class="col-3 text-center">
                                <button class="btn btn-sm btn-success">Follow Me</button>                                
                            </div>
                        </div>
                    `;
                    });
                }, 2000);
            }
            toFollowLoad = true;
        },
        error: function (error) {
            console.log(error);
        }
    });
  });
*/