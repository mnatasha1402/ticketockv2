




// app.use(router)
// app.mount('#main');
// Vue.createApp({
//   data(){
//       return {
//           footer: {patent:"© 2023 TICKETOCTS  ",creator:"By Natasha Mittal(21f1005823)"},
          
//       }
//   }
// }).mount("#footer"); 

const Home = Vue.component("home", {
    template: `
    
      <div>
        <div class="container mt-5">
          <h1 class="text-center">Welcome to Ticketocks</h1>
          <div class="d-flex justify-content-center">
            <a class="btn btn-warning mr-3"><router-link to="/user_login">User Login</router-link> </a>
            <a class="btn btn-warning"><router-link to="/admin_login">Admin Login</router-link></a>
          </div>
          <div>
            <center>
              <h3>Don't have an account? <router-link to="/signup">Sign Up</router-link></h3>
            </center>
          </div>
        </div>
        
      </div>
    `,
    data: function(){
        return {
            heading: ""
        };
    },
    mounted : function(){
        document.title= 'Welcome to Ticketocks';
        fetch("http://127.0.0.1:8001/")
        .then(response => response.json())
        .then(data => {
        this.heading = data["heading"];
        console.log(data)
      }
    )
        
}});
   

  


const Signup = Vue.component("signup", {
    template: `
      <div>
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-12 col-sm-8 col-md-6">
              <div class="card elevation-12">
                <div class="toolbar-primary">
                  <h5 class="toolbar-title">Sign Up</h5>
                </div>
                <div class="card-body">
                  <form>
                  <div class="form-group">
                  <label for="user_type">User Type:</label>
                  <select class="form-control" id="user_type" v-model="user_type">
                    <option value="admin">Admin</option>
                    <option value="user">User</option>
                    </select>
                    </div>
                    <div class="form-group">
                      <label for="username">Username</label>
                      <input type="text" class="form-control" id="username" v-model="username">
                    </div>
                    <div class="form-group">
                      <label for="email">Email</label>
                      <input type="email" class="form-control" id="email" v-model="email">
                    </div>
                    <div class="form-group">
                      <label for="password">Password</label>
                      <input type="password" class="form-control" id="password" v-model="password">
                    </div>
                  </form>
                </div>
                <div class="card-footer">
                  <button class="btn btn-primary" @click="signup">Sign Up</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>`,
    data() {
      return {
        user_type:"",
        username: "",
        email: "",
        password: "",
        is_authenticated: false,
        authenticated:true
      };
    },
    mounted: function () {
      document.title = "Sign-up";
    },
    methods: {
      async signup() {
        const response = await fetch("http://127.0.0.1:8001/signup", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            user_type:this.user_type,
            username: this.username,
            email: this.email,
            password: this.password
          })
        });
  
        const data = await response.json();
  
        if (response.ok) {
          this.authenticated=true
          this.is_authenticated=true
  
          this.$router.push("/");
        } else {
          this.err = data.message;
        }
      }
    }
  });

  const UserLogin = Vue.component("user-login", {
    template: `
      <div class="container my-5">
        <h1 class="text-center">User Login</h1>
        <form @submit="login" id="user_login">
          <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" class="form-control" id="username" v-model="username" required>
          </div>
          <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" class="form-control" id="password" v-model="password" required>
          </div>
          <button type="submit" class="btn btn-primary">Login</button>
        </form>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </div>
    `,
    data() {
      return {
        username: "",
        password: "",
        errorMessage:''
      };
    },
    mounted: function () {
      document.title = "User Login";
    },
    methods: {
      async login(event) {
        event.preventDefault();
        try {
          const response = await fetch("http://127.0.0.1:8001/user_login", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password,
            }),
          });
      
          // Check if the response status is in the range of 200-299 (successful response)
          if (response.ok) {
            const data = await response.json();
            console.log(data);
      
            localStorage.setItem('authToken', data.access_token);
            localStorage.setItem('user_id', data.userid);
            localStorage.setItem('user_type', "user");
            localStorage.setItem('username', this.username);
      
            this.$router.push('/user_dashboard');
          } else {
            // Handle the error when the server responds with an error status
            console.error('Error:', response.status, response.statusText);
            this.errorMessage = "Invalid credentials";
            this.username= "",
            this.password= ""
          }
        } catch (error) {
          console.error("Invalid credentials", error);
          this.errorMessage = "Invalid credentials";
          console.log(errorMessage)
        }
      },
    }
  })

  const AdminLogin = Vue.component("admin-login", {
    template: `
    <div class="container my-5">
    <h1 class="text-center">Admin Login</h1>
    <form @submit="login" id="admin_login">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" class="form-control" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" class="form-control" id="password" v-model="password" required>
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
    <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
  </div>
    `,
    mounted() {
      document.title = "Admin Login";
      // Additional logic or API calls can be added here
    },
    data() {
      return {
        username: "",
        password: "",
        errorMessage:""
      };
    },
    methods: {
      async login(event) {
        event.preventDefault();
        try {
          const response = await fetch("http://127.0.0.1:8001/admin_login", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password,
            }),
          });
      
          // Check if the response status is in the range of 200-299 (successful response)
          if (response.ok) {
            const data = await response.json();
            console.log(data);
      
            localStorage.setItem('authToken', data.access_token);
            localStorage.setItem('user_id', data.admin_id);
            localStorage.setItem('user_type', "admin");
            localStorage.setItem('username', this.username);
      
            this.$router.push('/admin_dashboard');
          } else {
            // Handle the error when the server responds with an error status
            console.error('Error:', response.status, response.statusText);
            this.errorMessage = "Invalid credentials";
            this.username= "",
            this.password= ""
          }
        } catch (error) {
          console.error("Invalid credentials", error);
          this.errorMessage = "Invalid credentials";
          console.log(errorMessage)
        }
      },
    }
  });
  

  const UserDashboard = Vue.component("user-dashboard", {
    template: `
      <div class="container">
        <h1 class="text-center">Welcome to Ticketocks</h1>
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-md-6">
              <!-- Content for the user dashboard -->
            </div>
          </div>
        </div>
        <div class="text-center">
          <router-link to="/venues" class="btn btn-primary">Venues</router-link>
          <router-link to="/shows" class="btn btn-primary">Shows</router-link>
        </div>
      </div>
    `,
    mounted() {
      document.title = "User Dashboard";
      // Additional logic or API calls can be added here
    }
  });

  const AdminDashboard = Vue.component("admin-dashboard", {
    template: `
      <div class="container">
        <h1 class="text-center">Admin Dashboard</h1>
        <div class="text-center">
          <router-link to="/venue_mgt" class="btn btn-primary">Venue Management</router-link>
          <router-link to="/add_venue" class="btn btn-primary">Add Venue</router-link>
        </div>
      </div>
    `,
    mounted() {
      document.title = "Admin Dashboard";
      // Additional logic or API calls can be added here
    }
  });

  const Shows = Vue.component("shows", {
    template: `
      <div class="container">
        <form @submit.prevent="searchShows" class="mb-3">
          <input type="text" class="search-text" v-model="searchQuery" placeholder="Search show">
          <input type="number" class="search-text" v-model.number="ratingFilter" placeholder="rating 1-5" pattern="[1-5]{1}" title="Rating from 1-5">
          <select class="search-text" v-model="tagFilter" placeholder="Search by tag">
          <option value="">All Tags</option>
          <option v-for="tag in tags" :value="tag">{{ tag }}</option>
          </select>
          
          <button type="button" class="btn" @click="resetFilters">Reset</button>
        </form>
  
        <h1 class="text-center">Shows</h1>
  
        <table class="table table-striped">
          <thead class="thead-dark">
            <tr>
              <th>S No.</th>
              <th>Name</th>
              <th>Date and Time</th>
              <th>Venue</th>
              <th>Ratings</th>
              <th>Tags</th>
              <th>Ticket Price</th>
              <th>Available Tickets</th>
              <th>Book</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(show, index) in filteredShows" :key="show.id">
              <td>{{ index + 1 }}</td>
              <td>{{ show.name }}</td>
              <td>{{ show.date }}<br>{{ show.time }}</td>
              <td>{{ show.venue }}</td>
              <td>{{ show.rating }}</td>
              <td>{{ show.tags }}</td>
              <td>{{ show.ticket_price }}</td>
              <td v-if="show.available_tickets <= 0">
                <h5><font color="red">HOUSEFULL</font></h5>
              </td>
              <td v-else>{{ show.available_tickets }}</td>
              <td v-if="show.available_tickets <= 0">
                <button type="button" class="btn btn-danger" disabled>Book Show</button>
              </td>
              <td v-else>
                <router-link :to="'/booking_form/' + show.id" class="btn btn-danger">Book Show</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    `,
    data() {
      return {
        shows: [], // Array of shows data
        tags:[],
        searchQuery: "", // Search input value
        ratingFilter: null, // Rating filter value
        tagFilter: "", // Tag filter value
        user_id:''
      };
    },
    mounted() {
      document.title = "Shows";
      // Additional logic or API calls can be added here to fetch the shows data
      const auth_token=localStorage.getItem('authToken');
      const user_id=localStorage.getItem('user_id')
      if (auth_token)
        fetch("http://127.0.0.1:8001/shows",{
          headers: {
            Authorization: `Bearer ${auth_token}` // Include the JWT token in the Authorization header
          }
        })
          .then(response=> {
            if (!response.ok) {
              throw new Error("Unauthorized"); // Throw an error if the response is not successful
            }
            return response.json();
          })
          .then(data => {
          this.shows = data["shows"];
          this.tags = [...new Set(this.shows.map(show => show.tags))];
          // this.venue=data["venue"]
          console.log(data);
      // Example: fetch shows data from an API endpoint and assign it to the 'shows' data property
      // this.shows = ...
    })
    },
    computed: {
      filteredShows() {
        // Filter shows based on search query, rating, and tag
        return this.shows.filter(show => {
          const searchMatch = show.name.toLowerCase().includes(this.searchQuery.toLowerCase());
          const ratingMatch = !this.ratingFilter || show.rating === this.ratingFilter;
          const tagMatch = show.tags.toLowerCase().includes(this.tagFilter.toLowerCase());
          return searchMatch && ratingMatch && tagMatch;
        });
      }
    },
    methods: {
      searchShows() {
        // Perform search action based on filters
        // Example: Fetch shows data from an API
        // and assign the result to the 'shows' data property
    },
    resetFilters() {
      // Reset all filters to their default values
      this.searchQuery = "";
      this.ratingFilter = null;
      this.tagFilter = "";
    }
  }
});
  

const Venues = Vue.component("venues", {
  template: `
    <div class="container mt-5">
      <form  class="mb-3">
        <input type="text" class="search-text" v-model="searchQuery" placeholder="Search venue" name="search">
        <select class="btn" v-model="locationFilter" name="location_filter">
          <option value="">All Locations</option>
          <option v-for="location in locations" :value="location">{{ location }}</option>
        </select>
         
        <button type="button" class="btn" @click="resetFilters">Reset</button>
      </form>
      
      <h1 class="text-center">Venues</h1>
      <table class="table table-striped">
        <thead class="thead-dark">
          <tr>
            <th>S No.</th>
            <th>Name</th>
            <th>Place</th>
            <th>Capacity</th>
            <th>Shows</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(venue, index) in filteredVenues" :key="venue.id">
            <td>{{ index + 1 }}</td>
            <td>{{ venue.name }}</td>
            <td>{{ venue.place }}</td>
            <td>{{ venue.capacity }}</td>
            <td>
              <router-link :to="'/venues/' + venue.id" class="btn btn-danger">See Shows</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  `,
  data() {
    return {
      venues: [], // Array of venue data
      locations: [], // Array of available locations
      searchQuery: "", // Search input value
      locationFilter: "" // Location filter value
    };
  },
  mounted() {
    document.title = "Venues";
    // Additional logic or API calls can be added here to fetch the venues data and available locations
    const auth_token=localStorage.getItem('authToken');
    const user_id=localStorage.getItem('user_id')
    if (auth_token)
      fetch("http://127.0.0.1:8001/venues",{
        headers: {
          Authorization: `Bearer ${auth_token}` // Include the JWT token in the Authorization header
        }
      })
          .then(response=> {
            if (!response.ok) {
              throw new Error("Unauthorized"); // Throw an error if the response is not successful
            }
            return response.json();
          })
          .then(data => {
          this.venues = data["venues"];
          this.locations = [...new Set(this.venues.map(venue => venue.place))];
    // Example: fetch venues data from an API endpoint and assign it to the 'venues' data property
    // Example: fetch available locations from an API endpoint and assign it to the 'locations' data property
    })
  },
  computed: {
    filteredVenues() {
      // Filter venues based on search query and location
      return this.venues.filter(venue => {
        const searchMatch = venue.name.toLowerCase().includes(this.searchQuery.toLowerCase());
        const locationMatch = !this.locationFilter || venue.place === this.locationFilter;
        return searchMatch && locationMatch;
      });
    }
  },
  methods: {
    searchVenues() {
      // Perform search action based on filters
      // Example: Fetch venues data from an API endpoint based on the filters
      // and assign the result to the 'venues' data property
      const authToken = localStorage.getItem('authToken');
      const url = `http://127.0.0.1:8001/venues?search=${this.searchQuery}&location_filter=${this.locationFilter}`;

    fetch(url,{
      headers: {
        Authorization: `Bearer ${authToken}` // Include the JWT token in the Authorization header
      }
    })
      .then(response => response.json())
      .then(data => {
        this.venues = data.venues;
      })
      .catch(error => {
        console.error("Error searching venues:", error);
      });
    },
    resetFilters() {
      // Reset all filters to their default values
      this.searchQuery = "";
      this.locationFilter = "";
    }
  }
});

const VenueDetails= Vue.component('VenueDetails', {
  // props: {
  //   venue: {
  //     type: Object,
  //     required: true
  //   },
  //   shows: {
  //     type: Array,
  //     required: true
  //   },
  //   venueId: {
  //     type: Number,
  //     required: true
  //   }
  // },
  template: `
    <div>
    <div class="ven">
      <center>
        <h1>{{ venue.name }}</h1>
        <h5>Location: {{ venue.place }}</h5>
        <h5>Capacity: {{ venue.capacity }}</h5>
      </center>
    </div>
    <div class="container">
      <form  class="mb-3">
        <input type="text" class="search-text" v-model="searchQuery" placeholder="Search show" name="search">
        <input type="number" class="search-text" v-model="ratingFilter" placeholder="Rating 1-5" pattern="[1-5]{1}" title="Rating from 1-5" name="rating">
        <select class="search-text" v-model="tagFilter" placeholder="Search by tag">
          <option value="">All Tags</option>
          <option v-for="tag in tags" :value="tag">{{ tag }}</option>
          </select>
        
        <button type="button" class="btn" @click="resetFilters">Reset</button>
      </form>

      <h1 class="text-center">Shows in {{ venue.name }}</h1>

      <table class="table table-striped">
        <thead class="thead-dark">
          <tr>
            <th>S No.</th>
            <th>Name</th>
            <th>Venue</th>
            <th>Ratings</th>
            <th>Tags</th>
            <th>Ticket Price</th>
            <th>Available Tickets</th>
            <th>Book</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(show, index) in filteredShows" :key="show.id">
            <td>{{ index + 1 }}</td>
            <td>{{ show.name }}</td>
            <td>{{ venue.name }}</td>
            <td>{{ show.rating }}</td>
            <td>{{ show.tags }}</td>
            <td>{{ show.ticket_price }}</td>
            <td v-if="show.available_tickets <= 0">
              <h5><font color="red">HOUSEFULL</font></h5>
            </td>
            <td v-else>
              {{ show.available_tickets }}
            </td>
            <td v-if="show.available_tickets <= 0">
              <button type="button" class="btn btn-danger disabled">Book Show</button>
            </td>
            <td v-else>
              
              <router-link :to="'/booking_form/' + show.id" class="btn btn-danger">Book Show</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  `,
  data() {
    return {
      venue:'',
      shows:[],
      tags:[],
      searchQuery: '',
      ratingFilter: '',
      tagFilter: ''
    };
  },
  mounted(){
    document.title = "Shows at {{ venue.name }}";
    // Additional logic or API calls can be added here to fetch the venues data and available locations
    const auth_token=localStorage.getItem('authToken');
    const user_id=localStorage.getItem('user_id')
    const venue_id = this.$route.params.venue_id;
    if (auth_token)
      fetch(`http://127.0.0.1:8001/venues/${this.$route.params.venue_id}`,{
        headers: {
          Authorization: `Bearer ${auth_token}` // Include the JWT token in the Authorization header
        }
      })
          .then(response=> {
            if (!response.ok) {
              throw new Error("Unauthorized"); // Throw an error if the response is not successful
            }
            return response.json();
          })
          .then(data => {
          this.venue = data["venue"];
          this.shows = this.venue.shows;
          this.tags = [...new Set(this.shows.map(show => show.tags))];
          console.log(data)
    // Example: fetch venues data from an API endpoint and assign it to the 'venues' data property
    // Example: fetch available locations from an API endpoint and assign it to the 'locations' data property
    })
  },
  
  computed: {
    filteredShows() {
      return this.shows.filter((show) => {
        const searchMatch = show.name.toLowerCase().includes(this.searchQuery.toLowerCase());
        const ratingMatch = !this.ratingFilter || show.rating === parseInt(this.ratingFilter);
        const tagMatch = !this.tagFilter || show.tags.includes(this.tagFilter);
        return searchMatch && ratingMatch && tagMatch;
      });
    }
  },
  methods: {
    searchShows() {
      // Implement the logic to fetch shows data based on the filters
      // You can make an API request and update the 'shows' data property with the filtered results
      // Example:
      // fetch(`http://your-api-endpoint?search=${this.searchQuery}&rating=${this.ratingFilter}&tag=${this.tagFilter}`)
      //   .then(response => response.json())
      //   .then(data => {
      //     this.shows = data.shows;
      //   })
      //   .catch(error => {
      //     console.error('Error fetching shows:', error);
      //   });
    },
    resetFilters() {
      this.searchQuery = '';
      this.ratingFilter = '';
      this.tagFilter = '';
    }
  }
});

const BookingForm = Vue.component('BookingForm', {
  template: `
  <div class="container">
    <h1 class="text-center mt-5">Booking for {{ show.name }} <br> <h3><center>on {{ show.date }}, {{ show.time }}</center></h3></h1>
    <form @submit.prevent="confirmBooking">
      <div class="form-group">
        <label for="available_tickets">Tickets available:</label>
        <span id="available_tickets"> {{ show.available_tickets }} </span>
      </div>
      <div class="form-group">
        <label for="num_tickets">Number of Tickets:</label>
        <input type="number" class="form-control" v-model="numTickets" required />
        <p v-if="showError" class="text-danger">Number of tickets exceeds available tickets.</p>
      </div>
      <div class="form-group">
        <label for="price">Price per Ticket:</label>
        <input type="number" class="form-control" step="0.01" v-model="ticketPrice" readonly />
      </div>
      <button type="submit" class="btn btn-primary">Confirm Booking</button>
      <p v-if="showConfirmation" class="text-success">Booking confirmed!</p>
      <div v-if="bookingStatus === 'success'" class="alert alert-success mt-3">
      Booking successful!
      </div>

    </form>
  </div>
`,
  data() {
    return {
      show: {},
      user: {},
      numTickets: '',
      ticketPrice: '',
      showError: false,
      showConfirmation: false,
      bookingStatus: null 
    };
  },
  mounted() {
    document.title='Booking Form'
    const auth_token = localStorage.getItem('authToken');
    const user_id = localStorage.getItem('user_id');
    if (auth_token) {
      fetch(`http://127.0.0.1:8001/booking_form/${this.$route.params.show_id}`, {
        headers: {
          Authorization: `Bearer ${auth_token}`
        }
      })
        .then(response => {
          if (!response.ok) {
            throw new Error("Unauthorized");
          }
          return response.json();
        })
        .then(data => {
          this.show = data.show;
          this.user = data.user;
          this.numTickets = '';
          this.ticketPrice = this.show.ticket_price;
          console.log(data)
        })
        .catch(error => {
          console.error('Error fetching booking form:', error);
        });
    }
  },
  computed: {
    availableTickets() {
      return this.show.available_tickets;
    }
  },
  methods: {
    confirmBooking() {
      const auth_token = localStorage.getItem('authToken');
      const user_id = localStorage.getItem('user_id');
      if (auth_token) {
        const num_tickets = parseInt(this.numTickets);
        const ticket_price = parseFloat(this.ticketPrice);
        const total_price = num_tickets * ticket_price;

        if (num_tickets > this.availableTickets) {
          this.showError = true;
          this.showConfirmation = false;
          return;
        }

        const confirmationMessage = `Total price is ${total_price}. Confirm booking?`;
        if (confirm(confirmationMessage)) {
        const booking_data = {
          num_tickets: num_tickets,
          total_price: total_price
        };
      
        fetch(`http://127.0.0.1:8001/booking_form/${this.$route.params.show_id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${auth_token}`
          },
          body: JSON.stringify(booking_data)
        })
          .then(response => {
            if (!response.ok) {
              throw new Error("Booking failed");
            }
            return response.json();
          })
          .then(data => {
            this.showConfirmation = true;
            this.showError = false;
            this.bookingStatus = 'success'; 
            this.user_id=user_id;
            console.log('Booking successful:', data);
            //this.$router.push(`/invoice/${user_id}/${booking_id}`)
             this.$router.push(`/bookings/${user_id}`)
          })
          .catch(error => {
            console.error('Error confirming booking:', error);
          });
        }
      }
    }
  }
});

const Bookings = Vue.component('Bookings', {
  template: `
    <div class="container mt-5">
      <h1 class="text-center">{{ user.name }}'s bookings</h1>
      <table v-if="bookings && bookings.length > 0" class="table table-striped">
        <thead class="thead-dark">
          <tr>
            <th>Show Name</th>
            <th>Venue</th>
            <th>Date</th>
            <th>Time</th>
            <th>Number of Tickets</th>
            <th>Total Price</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in bookings" :key="booking.id">
            <td>
              {{ booking.show_name }}
              <br>
              <small class="text-muted">booked on: {{booking.booking_time}}</small>
            </td>
            <td>{{ booking.venue_name }}</td>
            <td>{{ booking.show_date }}</td>
            <td>{{ booking.show_time }}</td>
            <td>{{ booking.num_tickets }}</td>
            <td>{{ booking.total_price }}</td>
            <td>
             <router-link :to="'/invoice/' + user.id+'/' + booking.bookingId" class="btn btn-danger">View Invoice</router-link>
              <button class="btn btn-danger" @click="cancelBooking(booking.bookingId,booking.show_id,booking.num_tickets)">Cancel Booking</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>You have no bookings yet.</p>
    </div>
  `,
  data() {
    return {
      user: {},
      bookings: []
    };
  },
  mounted() {
    document.title = "My Bookings";
    const auth_token = localStorage.getItem('authToken');
    const user_id = localStorage.getItem('user_id');
    if (auth_token) {
      fetch(`http://127.0.0.1:8001/bookings/${user_id}`, {
        headers: {
          Authorization: `Bearer ${auth_token}`
        }
      })
        .then(response => {
          if (!response.ok) {
            throw new Error("Unauthorized");
          }
          return response.json();
        })
        .then(data => {
          this.user = data.user;
          this.bookings = data.bookings;
        })
        .catch(error => {
          console.error('Error fetching bookings:', error);
        });
    }
  },
  methods: {
    cancelBooking(bookingId) {
      const auth_token = localStorage.getItem('authToken');
      if (auth_token) {
        if (confirm("Are you sure you want to cancel this booking?")) {
          fetch(`http://127.0.0.1:8001/bookings/delete/${bookingId}`, {
            method: 'DELETE',
            headers: {
              Authorization: `Bearer ${auth_token}`
            }
          })
            .then(response => {
              if (!response.ok) {
                throw new Error("Failed to cancel booking");
              }
              return response.json();
            })
            .then(data => {
              // Refresh the bookings after cancellation
              this.fetchBookings();
              console.log('Booking cancelled:', data);
              // Increase the number of available tickets for the show
              // const showId = show_id; // Replace `show_id` with the actual property name
              // const numTicketsCancelled = num_tickets; // Replace `num_tickets` with the actual property name
              // this.increaseAvailableTickets(showId, numTicketsCancelled);
            })
            .catch(error => {
              console.error('Error cancelling booking:', error);
            });
        }
      }
    },
    // increaseAvailableTickets(showId, numTicketsCancelled) {
    //   const auth_token = localStorage.getItem('authToken');
    //   if (auth_token) {
    //     fetch(`http://127.0.0.1:8001/shows/increase_tickets/${showId}`, {
    //       method: 'PUT',
    //       headers: {
    //         Authorization: `Bearer ${auth_token}`,
    //         'Content-Type': 'application/json'
    //       },
    //       body: JSON.stringify({
    //         numTicketsCan: numTicketsCancelled
    //       })
    //     })
    //       .then(response => {
    //         if (!response.ok) {
    //           throw new Error("Failed to increase available tickets");
    //         }
    //         return response.json();
    //       })
    //       .then(data => {
    //         console.log('Available tickets increased:', data);
    //       })
    //       .catch(error => {
    //         console.error('Error increasing available tickets:', error);
    //       });
    //   }
    // },

    fetchBookings() {
      const auth_token = localStorage.getItem('authToken');
      const user_id = localStorage.getItem('user_id');
      if (auth_token) {
        fetch(`http://127.0.0.1:8001/bookings/${user_id}`, {
          headers: {
            Authorization: `Bearer ${auth_token}`
          }
        })
          .then(response => {
            if (!response.ok) {
              throw new Error("Unauthorized");
            }
            return response.json();
          })
          .then(data => {
            this.user = data.user;
            this.bookings = data.bookings;
          })
          .catch(error => {
            console.error('Error fetching bookings:', error);
          });
      }
    }
  }
});

const Invoice = Vue.component('invoice', {
  template: `
  <div class="invoice">
  <h1>Invoice</h1>
  <img src="./static/QR.png" alt="invoice">
  <div class="invoice-details">
    <table>
      <tr>
        <td><b>Booking ID:</b></td>
        <td>{{ booking.bookingId }}</td>
      </tr>
      <tr>
        <td><b>Name:</b></td>
        <td>{{ user.name }}</td>
      </tr>
      <tr>
        <td><b>Booking Date:</b></td>
        <td>{{ booking.show_date }}</td>
      </tr>
      <tr>
        <td><b>Booking Time:</b></td>
        <td>{{ booking.show_time }}</td>
      </tr>
      <tr>
        <td><b>Booking Venue:</b></td>
        <td>{{ booking.venue_name }}</td>
      </tr>
      <tr>
        <td><b>Booking Show:</b></td>
        <td>{{ booking.show_name }}</td>
      </tr>
      <tr>
        <td><b>Number of Tickets:</b></td>
        <td>{{ booking.num_tickets }}</td>
      </tr>
      <tr>
        <td><b>Total Price:</b></td>
        <td>{{ booking.total_price }}</td>
      </tr>
    </table>
    <button class="btn btn-danger" style="margin-top: 20px;" @click="cancelBooking(booking.bookingId,booking.show_id,booking.num_tickets)">Cancel Booking</button>
    
  </div>
  </div>
  `,
  data() {
    return {
      user: {},
      booking: [],
      // show: {
      //   show_date: '',
      //   show_time: ''
      // }
    };
  },
  methods: {
      
    invoiceImage() {
      // Generate the URL for the invoice image
      return window.location.pathname + '/static/QR.png';
    },
    cancelBooking(booking_id) {
      const auth_token = localStorage.getItem('authToken');
      const user_id = localStorage.getItem('user_id');
      if (auth_token) {
        if (confirm("Are you sure you want to cancel this booking?")) {
          fetch(`http://127.0.0.1:8001/bookings/delete/${booking_id}`, {
            method: 'DELETE',
            headers: {
              Authorization: `Bearer ${auth_token}`
            }
          })
            .then(response => {
              if (!response.ok) {
                throw new Error("Failed to cancel booking");
              }
              return response.json();
            })
            .then(data => {
              // Refresh the bookings after cancellation
              this.fetchBookings();
              console.log('Booking cancelled:', data);
              this.$router.push(`/bookings/${user_id}`)
              // Increase the number of available tickets for the show
              // const showId = show_id; // Replace `show_id` with the actual property name
              // const numTicketsCancelled = num_tickets; // Replace `num_tickets` with the actual property name
              // this.increaseAvailableTickets(showId, numTicketsCancelled);
            })
            .catch(error => {
              console.error('Error cancelling booking:', error);
            });
        }
      }
    },
    fetchBookings() {
      const auth_token = localStorage.getItem('authToken');
      const user_id = localStorage.getItem('user_id');
      if (auth_token) {
        fetch(`http://127.0.0.1:8001/bookings/${user_id}`, {
          headers: {
            Authorization: `Bearer ${auth_token}`
          }
        })
          .then(response => {
            if (!response.ok) {
              throw new Error("Unauthorized");
            }
            return response.json();
          })
          .then(data => {
            this.user = data.user;
            this.bookings = data.bookings;
          })
          .catch(error => {
            console.error('Error fetching bookings:', error);
          });
      }
    }
  },

  mounted() 
  {
    document.title = "Invoice";
    const auth_token = localStorage.getItem('authToken');
    const user_id = localStorage.getItem('user_id');
    const booking_id = this.$route.params.bookingId
    if (auth_token) {
      fetch(`http://127.0.0.1:8001/bookings/${user_id}/${booking_id}`, {
        headers: {
          Authorization: `Bearer ${auth_token}`
        }
      })
        .then(response => {
          if (!response.ok) {
            throw new Error("Unauthorized");
          }
          return response.json();
        })
        .then(data => {
          this.user = data.user;
          this.booking = data.booking;
          console.log(data)
        })
        .catch(error => {
          console.error('Error fetching booking:', error);
        });
    }  
  }
});


const VenueManagement = Vue.component('VenueManagement', {
  template: `
    <div class="container">
      <h1>Venue Management</h1>
      <router-link to="/add_venue" class="btn btn-primary">Create Venue</router-link>
      <form @submit.prevent="searchVenue">
        <input type="text" class="search-text" v-model="searchQuery" placeholder="Search venue">
        
        <button type="button" class="btn" @click="resetSearch">Reset</button>
      </form>

      <table  v-if="filteredVenues && filteredVenues .length > 0" class="table table-striped">
        <thead>
          <tr>
            <th>S No.</th>
            <th>Name</th>
            <th>Place</th>
            <th>Capacity</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(venue, index) in filteredVenues " :key="venue.id">
            <td>{{ index + 1 }}</td>
            <td>{{ venue.name }}</td>
            <td>{{ venue.place }}</td>
            <td>{{ venue.capacity }}</td>
            <td>
              <button @click="deleteVenue(venue.id)" class="btn btn-danger">Delete</button>
              <router-link :to="'/edit_venue/' + venue.id" class="btn btn-warning">Edit</router-link>
              
              <router-link :to="'/add_show/' + venue.id" class="btn btn-warning">Add Show</router-link>
              <router-link :to="'/show_mgt/' + venue.id" class="btn btn-warning">See Shows</router-link>

            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>You have no venues yet.</p>
    </div>
  `,
  data() {
    return {
      searchQuery: '',
      venues: []
    };
  },
  computed: {
    filteredVenues() {
      if (this.searchQuery) {
        return this.venues.filter(venue =>
          venue.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          venue.place.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      } else {
        return this.venues;
      }
    }
  },
  methods: {
    searchVenue() {
      console.log('Search query:', this.searchQuery);
    },
    resetSearch() {
      this.searchQuery = '';
    },
    deleteVenue(venueId) {
      const auth_token = localStorage.getItem('authToken');
      if (auth_token) {
        if (confirm("Are you sure you want to delete this venue?")) {
          fetch(`http://127.0.0.1:8001/venue_mgt/delete/${venueId}`, {
            method: 'DELETE',
            headers: {
              Authorization: `Bearer ${auth_token}`
            }
          })
            .then(response => {
              if (!response.ok) {
                throw new Error("Failed to delete venue");
              }
              return response.json();
            })
            .then(data => {
              // Refresh the bookings after cancellation
              this.fetchVenues();
              console.log('Venue Deleted:', data);
            })
            .catch(error => {
              console.error('Error deleting venue:', error);
            });
        }
      }
    },
    fetchVenues() {
      const auth_token = localStorage.getItem('authToken');
      const admin_id = localStorage.getItem('admin_id');
      const apiUrl = 'http://127.0.0.1:8001/venue_mgt'; 
      fetch(apiUrl, {headers: {
        Authorization: `Bearer ${auth_token}`
      }
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch venue data');
          }
          return response.json();
        })
        .then(data => {
          this.venues = data.venues;
        })
        .catch(error => {
          console.error('Error fetching venue data:', error);
        });
    }
  },
  mounted() {
    document.title='Venue Management'
    this.fetchVenues();
  }
});

const AddVenue = Vue.component('AddVenue', {
  template: `
    <div class="container">
      <h1 class="text-center mt-5">Add Venue</h1>
      <form @submit.prevent="addVenue" id="add_venue">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" class="form-control" id="name" v-model="venue.name" required />
        </div>
        <div class="form-group">
          <label for="place">Place:</label>
          <input type="text" class="form-control" id="place" v-model="venue.place" required />
        </div>
        <div class="form-group">
          <label for="capacity">Capacity:</label>
          <input type="number" class="form-control" id="capacity" v-model="venue.capacity" required />
        </div>
        <button type="submit" class="btn btn-primary">Add</button>
      </form>
    </div>
  `,
  data() {
    return {
      venue: {
        name: '',
        place: '',
        capacity: ''
      }
    };
  },
  methods: {
    addVenue() {
      const auth_token = localStorage.getItem('authToken');
      // Perform API call to add the venue
      const requestData = {
        name: this.venue.name,
        place: this.venue.place,
        capacity: this.venue.capacity
      };

      fetch('http://127.0.0.1:8001/add_venue', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${auth_token}`
        },
        body: JSON.stringify(requestData)
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`Failed to add venue (${response.status} ${response.statusText})`);
          }
          return response.json();
        })
        .then(data => {
          console.log('Venue added:', data);
          this.venue.name = '';
          this.venue.place = '';
          this.venue.capacity = null;
          this.$router.push(`/venue_mgt`)
        })
        .catch(error => {
          console.error('Error adding venue:', error);
        });
    }
  }
});

const EditVenue = Vue.component('EditVenue', {
  template: `
    <div class="container mt-5">
      <h1>Edit Venue</h1>
      <form @submit.prevent="updateVenue">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" class="form-control" id="name"  v-model="venue.name" required>
        </div>
        <div class="form-group">
          <label for="place">Place:</label>
          <input type="text" class="form-control" id="place" v-model="venue.place" required>
        </div>
        <div class="form-group">
          <label for="capacity">Capacity:</label>
          <input type="number" class="form-control" id="capacity" v-model="venue.capacity" required>
        </div>
        <button type="submit" class="btn btn-primary">Save Changes</button>
        <router-link to="/venue_mgt" class="btn btn-secondary">Cancel</router-link>
      </form>
    </div>
  `,
  data() {
    return {
      venue: {
        name: '',
        place: '',
        capacity: ''
      }
    };
  },
  methods: {
    updateVenue() {
      const venue_id = this.$route.params.venue_id;
      const requestData = {
        name: this.venue.name,
        place: this.venue.place,
        capacity: this.venue.capacity
      };

      const auth_token = localStorage.getItem('authToken');
      fetch(`http://127.0.0.1:8001/edit_venue/${venue_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${auth_token}`
        },
        body: JSON.stringify(requestData)
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`Failed to update venue (${response.status} ${response.statusText})`);
          }
          return response.json();
        })
        .then(data => {
          console.log('Venue updated:', data);
          // Redirect to venue management page
          this.$router.push('/venue_mgt');
        })
        .catch(error => {
          console.error('Error updating venue:', error);
        });
    },
    fetchVenue() {
      const venue_id = this.$route.params.venue_id;
      const auth_token = localStorage.getItem('authToken');

      fetch(`http://127.0.0.1:8001/edit_venue/${venue_id}`, {
        headers: {
          Authorization: `Bearer ${auth_token}`
        }
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch venue data');
          }
          return response.json();
        })
        .then(data => {
          console.log(data.venue)
          this.venue = data.venue;
        })
        .catch(error => {
          console.error('Error fetching venue data:', error);
        });
    }
  },
  mounted() {
    document.title = 'Edit Venue';
    this.fetchVenue();
  }
});

const ShowManagement_venue = Vue.component('ShowManagement_venue', {
  template: `
    <div class="container">
      <h1>Show Management for venue {{ venue.name }}</h1>
      <router-link :to="'/add_show/'+ venue.id" class="btn btn-warning">Add Show </router-link>
  
      <button class="btn btn-warning" @click="download_venueDetails">Download Venue Details</button>
      <form>
        <input type="text" class="search-text" v-model="searchQuery" placeholder="Search show" name="search">
        <input type="number" class="search-text" v-model="ratingFilter" placeholder="Rating 1-5" pattern="[1-5]{1}" title="Rating from 1-5" name="rating">
        <select class="search-text" v-model="tagFilter" placeholder="Search by tag">  
          <option v-for="tag in tags" :value="tag">{{ tag }}</option>
          <option value="">All Tags</option>
        </select>
        
        <button type="button" class="btn" @click="resetFilters">Reset</button>
      </form>

      

      <table v-if="filteredShows && filteredShows.length>0" class="table table-striped">
        <thead>
          <tr>
            <th>S No.</th>
            <th>Name</th>
            <th>Time and Date</th>
            <th>Venue</th>
            <th>Ratings</th>
            <th>Tags</th>
            <th>Ticket Price</th>
            <th>Available Tickets</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(show, index) in filteredShows" :key="show.id">
            <td>{{ index + 1 }}</td>
            <td>{{ show.name }}</td>
            <td>{{ show.date }}<br>{{ show.time }}</td>
            <td>{{ venue_name }}</td>
            <td>{{ show.rating }}</td>
            <td>{{ show.tags }}</td>
            <td>{{ show.ticket_price }}</td>
            <td>{{ show.available_tickets }}</td>
            <td>
            <router-link :to="'/edit_show/' + show.id" class="btn btn-warning">Edit Show</router-link>
            <button @click="deleteShow(show.id)" class="btn btn-danger">Delete</button>
            
            </td>
          </tr>
        </tbody>        
      </table>
      <p v-else>No shows in this venue.</p>
    </div>
  `,
  data() {
    return {
      venue_name: '', // Populate this with the venue name
      shows: [], // Populate this with the list of shows
      searchQuery: '', // Store the search query
      ratingFilter:'',
      tagFilter:'',
      venue: {
        id: '',
        name: ''
      },
      tags:[],
      admin_id:''
    };
  },
  computed: {
    filteredShows() {
      if (this.shows && this.shows.length > 0) {
        return this.shows.filter((show) => {
          const searchMatch = show.name.toLowerCase().includes(this.searchQuery.toLowerCase());
          const ratingMatch = !this.ratingFilter || show.rating === parseInt(this.ratingFilter);
          const tagMatch = !this.tagFilter || show.tags.includes(this.tagFilter);
          return searchMatch && ratingMatch && tagMatch;
        });
      } else {
        return [];
      }
    }
  },
  methods: {
    download_venueDetails() {
      this.download = false;
      const admin_id = localStorage.getItem('user_id');
      const venue_id = this.$route.params.venue_id;
      fetch(`http://127.0.0.1:8001/${admin_id}/${venue_id}/venue_details/download/`, {
        method: "GET",
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        }
      })
      .then(resp => {
        if (resp.ok) {
          return resp.json();
        } else {
          throw new Error('Failed to fetch data');
        }
      })
      .then(data => {
        if (data['msg'] === "Done") {
          this.download = true;
        }
      })
      .catch(error => {
        console.error('Error:', error);
        // Handle the error, show an error message to the user, etc.
      });
    
      setTimeout(() => this.download = false, 20000);
    },
    
    deleteShow(show_id) {
      const auth_token = localStorage.getItem('authToken');
      
      
      if (auth_token) {
        if (confirm("Are you sure you want to delete this show?")) {
          fetch(`http://127.0.0.1:8001/show_mgt_venue/delete/${show_id}`, {
            method: 'DELETE',
            headers: {
              Authorization: `Bearer ${auth_token}`
            }
          })
            .then(response => {
              if (!response.ok) {
                throw new Error("Failed to delete show");
              }
              return response.json();
            })
            .then(data => {
              // Refresh the bookings after cancellation
              this.fetchShows();
              console.log('Show Deleted:', data);
            })
            .catch(error => {
              console.error('Error deleting show:', error);
            });
        }
      }
    },
    searchShows() {
      // Perform search based on the search query
      console.log('Search query:', this.searchQuery);
    },
    resetSearch() {
      this.searchQuery = '';
      // Reset the search functionality here
    },
    fetchShows() {
      const venue_id = this.$route.params.venue_id;
      const auth_token = localStorage.getItem('authToken');
      const admin_id = localStorage.getItem('user_id');

      fetch(`http://127.0.0.1:8001/show_mgt/${venue_id}`, {
        headers: {
          Authorization: `Bearer ${auth_token}`
        }
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch show data');
          }
          return response.json();
        })
        .then(data => {
          if (data.shows && data.shows.length > 0) {
            this.shows = data.shows;
            this.tags = [...new Set(this.shows.map(show => show.tags))];
          } else {
            this.shows = [];
            this.tags = [];
          }
          this.venue_name = data.venue?.name || '';
          this.venue = data.venue;
          this.admin_id=admin_id;
        })
        .catch(error => {
          console.error('Error fetching show data:', error);
        });
      },
      resetFilters() {
        this.searchQuery = '';
        this.ratingFilter = '';
        this.tagFilter = '';
      }

  },
  mounted() {
    document.title = 'Show Management';
    this.fetchShows();
  }
});

const EditShow = Vue.component('EditShow', {
  template: `
    <div class="container">
      <h1 class="text-center my-5">Edit Show</h1>
      <form @submit.prevent="updateShow">
        <div class="form-group">
          <label for="name">Name</label>
          <input type="text" class="form-control" id="name" v-model="show.name">
        </div>
        <div class="form-group">
          <label for="date">Show Date:</label>
          <input type="date" id="date" class="form-control" v-model="show.date" required>
        </div>
        <div class="form-group">
          <label for="time">Show Time</label>
          <input type="time" id="time" class="form-control" value="show.time" v-model="show.time" required>
        </div>
        <div class="form-group">
          <label for="rating">Rating</label>
          <input type="number" step="0.1" min="0" max="10" class="form-control" id="rating" v-model="show.rating">
        </div>
        <div class="form-group">
          <label for="tags">Tags</label>
          <input type="text" class="form-control" id="tags" v-model="show.tags">
        </div>
        <div class="form-group">
          <label for="ticket_price">Ticket Price</label>
          <input type="number" step="0.01" min="0" class="form-control" id="ticket_price" v-model="show.ticket_price">
        </div>
        <div class="form-group">
          <label for="available_tickets">Available Tickets</label>
          <input type="number" min="0" class="form-control"  id="available_tickets" v-model="show.available_tickets" >
        </div>
        <button type="submit" class="btn btn-primary">Save Changes</button>
      </form>
    </div>
  `,
  data() {
    return {
      show: {
        name: '',
        date: '',
        time: '',
        rating: null,
        tags: '',
        ticket_price: null,
        available_tickets: null
      }
      // show:''
    };
  },
  methods: {
    updateShow() {
      const showId = this.$route.params.show_id;
      const requestData = {
        name: this.show.name,
        date: this.show.date,
        time: this.show.time,
        rating: this.show.rating,
        tags: this.show.tags,
        ticket_price: this.show.ticket_price,
        available_tickets: this.show.available_tickets
        
      };

      const auth_token = localStorage.getItem('authToken');
      fetch(`http://127.0.0.1:8001/edit_show/${showId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${auth_token}`
        },
        body: JSON.stringify(requestData)
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`Failed to update show (${response.status} ${response.statusText})`);
          }
          return response.json();
        })
        .then(data => {
          console.log('Show updated:', data);
          // Redirect to show management page
          this.$router.push('/show_mgt/');
        })
        .catch(error => {
          console.error('Error updating show:', error);
        });
    },
    fetchShow() {
      const showId = this.$route.params.show_id;
      const auth_token = localStorage.getItem('authToken');

      fetch(`http://127.0.0.1:8001/edit_show/${showId}`, {
        headers: {
          Authorization: `Bearer ${auth_token}`
        }
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch show data');
          }
          return response.json();
        })
        .then(data => {
          console.log(data.show)
          this.show = data.show;
        })
        .catch(error => {
          console.error('Error fetching show data:', error);
        });
    }
  },
  mounted() {
    document.title = 'Edit Show';
    this.fetchShow();
  }
});

const AddShow = Vue.component('AddShow', {
  template: `
    <div class="container">
      <h1 class="text-center mt-5">Add Show</h1>
      <form @submit.prevent="addShow" id="add_show" class="mt-5">
        <div class="form-group">
          <label for="name">Show Name:</label>
          <input type="text" name="name" id="name" v-model="show.name" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="date">Show Date:</label>
          <input type="date" name="date" id="date" v-model="show.date" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="time">Show Time</label>
          <input type="time" name="time" id="time" v-model="show.time" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="rating">Show Rating:</label>
          <input type="number" name="rating" id="rating" v-model="show.rating" class="form-control" pattern="[1-5]{1}" title="Rating from 1-5" required>
        </div>
        <div class="form-group">
          <label for="tags">Show Tags:</label>
          <input type="text" name="tags" id="tags" v-model="show.tags" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="ticket_price">Ticket Price:</label>
          <input type="number" name="ticket_price" id="ticket_price" v-model="show.ticket_price" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="available_tickets">Available Tickets:</label>
          <input type="number" name="available_tickets" id="available_tickets" v-model="show.available_tickets" class="form-control" required>
          <p v-if="show.available_tickets > remainingCapacity" class="text-danger">Number of tickets exceeds venue capacity.</p>
        </div>
        <div class="form-group">
          <label for="venue_name">Venue:</label>
          <input type="text" name="venue_name" id="venue_name" value="venue" v-model="venue.name" class="form-control" readonly>
        </div>
        <button type="submit" class="btn btn-warning">Add Show</button>
      </form>
    </div>
  `,
  data() {
    return {
      show: {
        name: '',
        date: '',
        time: '',
        rating: '',
        tags: '',
        ticket_price: '',
        available_tickets: ''
      },
      venue: {
        name: '',
        id:'',
        capacity: '',
        available_tickets_existing_shows: 0
      },
      showError: false,
      showConfirmation: false,
      remainingCapacity:0
    };
  },
  methods: {
    addShow() {
      const venueId = this.$route.params.venue_id;
      const remainingCapacity = this.venue.capacity - this.venue.available_tickets_existing_shows;

      if (this.show.available_tickets > remainingCapacity) {  
        this.showError = true;
        this.showConfirmation = false;
        return;
      }
      const requestData = {
        name: this.show.name,
        date: this.show.date,
        time: this.show.time,
        rating: this.show.rating,
        tags: this.show.tags,
        ticket_price: this.show.ticket_price,
        available_tickets: this.show.available_tickets
        
      };
      

      const auth_token = localStorage.getItem('authToken');
      fetch(`http://127.0.0.1:8001/add_show/${venueId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${auth_token}`
        },
        body: JSON.stringify(requestData)
      })
       .then(response => {
          if (!response.ok) {
            throw new Error(`Failed to add show (${response.status} ${response.statusText})`);
          }
          return response.json();
        })
        .then(data => {
          this.showConfirmation = true;
          this.showError = false;
          console.log('Show added:', data);
          this.show.name = '';
          this.show.date = '';
          this.show.time = '';
          this.show.rating = null;
          this.show.tags = '';
          this.show.ticket_price = null;
          this.show.available_tickets = '';
          this.$router.push('/show_mgt/' + venueId);

        })
        .catch(error => {
          console.error('Error adding show:', error);
        });
    },
    fetchVenue() {
      const venueId = this.$route.params.venue_id;
      const auth_token = localStorage.getItem('authToken');

      fetch(`http://127.0.0.1:8001/venues/${venueId}`, {
        headers: {
          Authorization: `Bearer ${auth_token}`
        }
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch venue data');
          }
          return response.json();
        })
        .then(data => {
          console.log(data)
          this.venue = data.venue;

          const totalAvailableTickets = data.venue.shows.reduce((total, show) => {
            return total + show.available_tickets;
          }, 0);
    
          this.venue.available_tickets_existing_shows = totalAvailableTickets;
          
        })
        .catch(error => {
          console.error('Error fetching venue data:', error);
        });
    }
  },
  mounted() {
    document.title = 'Add Show';
    this.fetchVenue();
  }
});

const admin_Profile= Vue.component('profile',{
  template: `
  <section class="vh-100" style="background-color:transparent;">
  <div class="container py-5 h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col-md-12 col-xl-4">

        <div class="card" style="border-radius: 15px;background-color:transparent; box-shadow: 0 14px 28px rgba(0,0,0,0.25);">
          <div class="card-body text-center">
            <div class="mt-4 mb-4 ">
              <div id="profileImage" >{{ profileInitials }}</div>
              
            </div>
            <h4 class="mb-2">{{ admin.username  }}</h4>
            <p class="text-muted mb-4">@user <span class="mx-2">|</span> <a>
                {{ admin.email }}</a></p>
            
            <button type="button" class="btn btn-primary btn-rounded btn-lg" @click="deleteAccount(admin.id)" >
              Delete Account
            </button>
            <div class="d-flex justify-content-between text-center mt-5 mb-2">
              <div>
                <p class="mb-2 h5">{{ admin.venues.length }}</p>
                <p class="text-muted mb-0">Venues created</p>
              </div>
              <div class="px-1">
                <p class="mb-2 h5">{{ admin.shows.length }}</p>
                <p class="text-muted mb-0">Shows created</p>
              </div>
              
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
  </section>
  `,
  data() {
    return {
      admin: {
        id:'',
        username:'',
        email:'',
        shows:'',
        venues:''
      },
      profileInitials: '',
    };
  },
  mounted() {
    document.title="Profile";
    // Fetch user details when the component is mounted
    this.fetchUser();
    

  },
  methods: {
    
    fetchUser() {
      // Replace 'user_id' with the actual user ID to fetch the user details
      const admin_id = this.$route.params.admin_id;
      const auth_token = localStorage.getItem('authToken');

      // Make a GET request to fetch user details
      fetch(`http://127.0.0.1:8001/profile/${admin_id}`, {
        headers: {
          Authorization: `Bearer ${auth_token}`, // Include the JWT token in the Authorization header if required
        },
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch user details');
          }
          return response.json();
        })
        .then(data => {
          console.log(data)
          this.admin = data; // Set the fetched user details to the 'user' object
          this.setProfileInitials();
          
        })
        .catch(error => {
          console.error('Error fetching user details:', error);
        });
    },

    setProfileInitials() {
      const firstName = this.admin.username;
      // const lastName = this.$refs.lastName.textContent;
      const initials = firstName.charAt(0).toUpperCase();
      this.profileInitials = initials;
      console.log(firstName)
    },
    deleteAccount(admin_id) {
        const auth_token = localStorage.getItem('authToken');
        if (auth_token) {
          if (confirm("Are you sure you want to delete this admin account?")) {
            fetch(`http://127.0.0.1:8001/delete_admin/${admin_id}`, {
              method: 'DELETE',
              headers: {
                Authorization: `Bearer ${auth_token}`
              }
            })
              .then(response => {
                if (!response.ok) {
                  throw new Error("Failed to delete account");
                }
                return response.json();
              })
              .then(data => {
                // Refresh the bookings after cancellation
                
                console.log('Account Deleted:', data);
                this.$router.push('/');
              })
              .catch(error => {
                console.error('Error deleting account:', error);
              });
          }
        }
      
    },
  }
})

const user_Profile= Vue.component('profile',{
  template: `
  <section class="vh-100" style="background-color:transparent;">
  <div class="container py-5 h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col-md-12 col-xl-4">

        <div class="card" style="border-radius: 15px;background-color:transparent; box-shadow: 0 14px 28px rgba(0,0,0,0.25);">
          <div class="card-body text-center">
            <div class="mt-4 mb-4 ">
              <div id="profileImage" >{{ profileInitials }}</div>
              
            </div>
            <h4 class="mb-2">{{ user.username  }}</h4>
            <p class="text-muted mb-4">@admin <span class="mx-2">|</span> <a>
                {{ user.email }}</a></p>
            
            <button type="button" class="btn btn-primary btn-rounded btn-lg" @click="deleteAccount(user.id)" >
              Delete Account
            </button>
            
              <div>
                <p class="mb-0 mt-3 h5">{{ user.bookings.length }}</p>
                <p class="text-muted mb-0 mt-0">Shows Booked</p>
              </div>
              
              
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
  </section>
  `,
  data() {
    return {
      user: {
        id:'',
        username:'',
        email:'',
        bookings:'',
        
      },
      profileInitials: '',
    };
  },
  mounted() {
    document.title="Profile";
    // Fetch user details when the component is mounted
    this.fetchUser();
    

  },
  methods: {
    
    fetchUser() {
      // Replace 'user_id' with the actual user ID to fetch the user details
      const user_id = this.$route.params.user_id;
      const auth_token = localStorage.getItem('authToken');

      // Make a GET request to fetch user details
      fetch(`http://127.0.0.1:8001/user_profile/${user_id}`, {
        headers: {
          Authorization: `Bearer ${auth_token}`, // Include the JWT token in the Authorization header if required
        },
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch user details');
          }
          return response.json();
        })
        .then(data => {
          console.log(data)
          this.user = data; // Set the fetched user details to the 'user' object
          this.setProfileInitials();
          
        })
        .catch(error => {
          console.error('Error fetching user details:', error);
        });
    },

    setProfileInitials() {
      const firstName = this.user.username;
      // const lastName = this.$refs.lastName.textContent;
      const initials = firstName.charAt(0).toUpperCase();
      this.profileInitials = initials;
      console.log(firstName)
    },
    deleteAccount(user_id) {
        const auth_token = localStorage.getItem('authToken');
        if (auth_token) {
          if (confirm("Are you sure you want to delete this user account?")) {
            fetch(`http://127.0.0.1:8001/delete_user/${user_id}`, {
              method: 'DELETE',
              headers: {
                Authorization: `Bearer ${auth_token}`
              }
            })
              .then(response => {
                if (!response.ok) {
                  throw new Error("Failed to delete account");
                }
                return response.json();
              })
              .then(data => {
                // Refresh the bookings after cancellation
                
                console.log('Account Deleted:', data);
                this.logout();
              })
              .catch(error => {
                console.error('Error deleting account:', error);
              });
          }
        }
      
    },
    logout() {
      this.authenticated=false
      // this.$router.go();
      localStorage.clear();
    
    this.$router.push('/');
    
  },
  }
})

  



const Navbar = Vue.component('navbar', {
  template: `
    <div id="nav" >
    <nav>
    <div class="navbar-logo">
      <img src="./static/img.png" alt="Your Logo">
    </div>
    <ul class="navbar-links">
      <li v-if=username><b><h5>Hi,{{ username }}!</h5></b></li>
      <li v-if="userType === 'admin'"><router-link :to="'/admin_profile/' + admin_id">My Profile</router-link></li>
      <li v-if="userType === 'user'"><router-link :to="'/user_profile/' + user_id">My Profile</router-link></li>
      <li v-if="userType === 'user'"><router-link to="/user_dashboard">Home</router-link></li>
      <li v-if="userType === 'user'"><router-link :to="'/bookings/' + user_id">My Bookings</router-link></li>
      <li v-if="userType === 'admin'"><router-link to="/admin_dashboard">Home</router-link></li>
      <li v-if="userType === 'admin'"><router-link to="/venue_mgt">Venue Management</router-link></li>
      <li v-if="userType === 'admin'"><button @click="logout()" class="btn btn-danger">Logout</button></li>
      <li v-if="userType === 'user'"><button @click="logout()" class="btn btn-danger">Logout</button></li>
    </ul>
  </nav>
    </div>
  `,
  data() {
    return {
      username: '', // Set the username dynamically based on the user
      userType: '', // Set the user type dynamically based on the user
      user_id: '', // Set the user ID dynamically based on the user
      admin_id:''
    };
  },
  methods: {
      
      logout() {
          this.authenticated=false
          // this.$router.go();
          localStorage.clear();
        
        this.$router.push('/');
        
      },
      post(){
          this.$router.push('/post_search');
      },
      user(){
          this.$router.push('/user_search');
      }
      
    },

  mounted() {
    this.username = localStorage.getItem('username'); // Example: Set the username
    this.userType = localStorage.getItem('user_type'); // Example: Set the user type
    this.user_id = localStorage.getItem('user_id'); 
    this.admin_id = localStorage.getItem('admin_id'); 

  }
});
  
  
  
  


  const routes=[
    
    {
        path: '/', 
        component: Home
    },

    {
      path: '/admin_login',
      component: AdminLogin
    },

    {
      path: '/user_login',
      component: UserLogin
    },

    { 
      path: '/signup',
      component: Signup
    },

    { 
      path: '/user_dashboard',
      component: UserDashboard
    },

    { 
      path: '/admin_dashboard',
      component: AdminDashboard
    },

    { 
      path: '/shows',
      component: Shows
    },

    // {
    //   path:'/shows/increase_tickets/:show_id',
    //   component:Shows
    // },

    { 
      path: '/venues',
      component: Venues
    },
    { 
      path: '/venues/:venue_id',
      component: VenueDetails
    },
    //   children: [
    //       {
    //         path:'/:venue_id',
    //         component:VenueDetails,
    //         // props:true
    //       },
    //   ]
    // },

    { 
      path: '/booking_form/:show_id',
      component: BookingForm
    },

    {
      path:'/bookings/:user_id',
      component:Bookings
    },

    {
      path:'/venue_mgt',
      component:VenueManagement
    },

    {
      path:'/add_venue',
      component:AddVenue
    },

    {
      path:'/edit_venue/:venue_id',
      component:EditVenue
    },

    {
      path:'/show_mgt/:venue_id',
      component:ShowManagement_venue
    },
    {
      path:'/add_show/:venue_id',
      component:AddShow
    },

    {
      path:'/edit_show/:show_id',
      component:EditShow
    },

    {
      path: '/invoice/:user_id/:bookingId',
      name: 'invoice',
      component: Invoice,
    },

    {
      path: '/admin_profile/:admin_id',
      component: admin_Profile,
    },

    {
      path: '/user_profile/:user_id',
      component: user_Profile,
    },
    
    // {
    //   path:'/bookings/delete/:bookingId',
    //   component:Bookings
    // }
    // {
    //   path: '/admin_dashboard/<int:admin_id',
    //   component : admin_dashboard,
    //   children: [
    //   {
    //     path:'/venues/<int:venue_id>',
    //     component:venue_mgt
    //   },
    //   {
    //     path:'shows/<int:venue_id>',
    //     component :show_mgt
    //   },
      
    //   ]
    // }
  
    
   
    
  ]

  const router = new VueRouter({
    // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
    // history: VueRouter.createWebHashHistory(),
    routes, // short for `routes: routes`
  })

  var app= new Vue({
    el:"#app",
    router
  //   data:{
  //       return: {
  //           footer: {patent:"© 2023 TICKETOCTS  ",creator:"By Natasha Mittal(21f1005823)"},
  //       }
  // }
  })

//   



//  app.use(Navbar)
// app.mount('#app');
//   Vue.createApp({
//     data(){
//         return {
//             footer: {patent:"© 2023 BLOG-LITE  ",creator:"By Utkarsh Gaurav(21f1001336)"},
            
//         }
//     }
//   }).mount("#footer"); 



  