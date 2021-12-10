$.ajax( {
    type: 'GET',
    url: '/gigs-json/',
    success: function (response) {
      console.log(response.data);
      const data = JSON.parse(response.data);
      console.log(data);
      data.forEach(el => {
        gigs2.innerHTML += `${el.fields.updated}`;
      });
    },
    error: function (error) {
      console.log(error);
    }
  });
  