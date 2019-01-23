// Author: Junior Tada

// inicializa vue
var app = new Vue({
    el: '#app1',

    data:{
    	clientes: [],
    	produtos: [],
    	cliente: '' 
    },

    mounted: function(){
    	this.$nextTick(function (){
	        this.buscarClientes();
  		})
    },

    methods: {
    	buscarClientes: function(event){
    		var self = this;
	        $.ajax({
	            url: '/financeiro/_clientes/',
	            method: 'GET',
	            success: function(data){
	                self.clientes = data.clientes;
	            },
	            error: function(error){
	                console.log(error);
	            }
	        });
    	},

    	buscarProdutos: function(event){

    	}
    }
});
