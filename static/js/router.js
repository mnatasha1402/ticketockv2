const routes=[
    
    {
        path: '/', 
        component: Home
    },

    {
      path: '/login/admin',
      component: login_admin
    },

    {
      path: '/login/user',
      component: login_user
    },

    { 
      path: '/signup',
      component: signup
    },

    {
      path: '/admin_dashboard/<int:admin_id',
      component : admin_dashboard,
      children: [
      {
        path:'/venues/<int:venue_id>',
        component:venue_mgt
      },
      {
        path:'shows/<int:venue_id>',
        component :show_mgt
      },
      
      ]
    }
  
    
   
    
  ]

  const router = VueRouter.createRouter({
    // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
    history: VueRouter.createWebHashHistory(),
    routes, // short for `routes: routes`
  })

  export default router