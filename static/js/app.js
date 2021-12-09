
// -- For card info box to collaps. From Bootstraps -- //
var collapseElementList = [].slice.call(document.querySelectorAll('.collapse'))
/*
var collapseList = collapseElementList.map(function (collapseEl) {
  return new bootstrap.Collapse(collapseEl)
})
*/

// -- Popover function -- //
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover-term"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})


// -- Activate welcome message -- //

console.log('Welcome!')
console.log(document)

const message = document.getElementById('message')
// const message2 = document.getElementById('message2')
console.log(message)

/*
setTimeout(() => {
  message.textContent = "Check out the lastest updates below."
}, 2000)
*/
/*
// -- Fetch json for gigs  -- //
$.ajax({
  type: 'GET',
  url: 'gig_json/',
  success: function(response) {
    console.log(response.data)
    const data = JSON.parse(response.data)
    console.log(data)
    setTimeout(() => {
      data.forEach(el=> {
        message2.innerHTML += `${el.fields.title}<br>`
      })
    }, 2000)
  },
  error: function(error) {
    console.log(error)
  }
})
*/


// -- To call the json data for industry --//
/*
var industryChoice = {
  id: fields._id_prof, 
  industry_name: fields.industry_name,
};


$.ajax({
  type: 'POST',
  url: 'userprofiles/fixtures/industry.json',
  contentType: 'application/json; charset=utf-8',
  data: $.toJSON(industryChoice),
  dataType: 'text',
  success: function (result) {
    alert(result.Result);
  }
});
*/