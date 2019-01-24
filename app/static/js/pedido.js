// Author: Junior Tada

// componentes
Vue.component('linha-item', {
 	props: ['linha'],
 	template: '<tr> \
	        	<td>{{linha.nome}}</td> \
	          	<td>{{linha.quantidade}}</td> \
	          	<td>{{dinheiro(linha.preco)}}</td> \
	          	<td>{{dinheiro(linha.total)}}</td> \
	          	<td class="centro">Boa</td> \
	          	<td class="centro"><button class="btn btn-danger btn-sm btn_excluir" @click="excluirItem(linha.id)"><i class="fas fa-times-circle"></i></button></td> \
	        </tr>',
    methods:{

    	excluirItem: function(id){
    		index = app.itens.indexOf(app.itens[id]);
    		app.itens.splice(index, 1);
    		console.log(app.itens);
    	}
    }

})

// inicializa vue
var app = new Vue({
    el: '#app1',

    data:{
    	clientes: [],
    	produtos: [],
    	itens: [],
    	cliente: '',
    	produto: '',
    	item: null 
    },

    mounted: function(){
    	this.$nextTick(function (){
	        this.buscarClientes();
	        this.buscarProdutos();
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
    		var self = this;
	        $.ajax({
	            url: '/financeiro/_produtos/',
	            method: 'GET',
	            success: function(data){
	                self.produtos = data.produtos;
	            },
	            error: function(error){
	                console.log(error);
	            }
	        });
    	},

    	produtoSelecionado: function(event){
    		var self = this;
    		self.item = self.produtos[self.produto -1];
    		// set preço
    		$('#preco').val(dinheiro(self.item.preco));
    		// valida e set multiplo
    		if(self.item.multiplo){
    			$('#quantidade').val(self.item.multiplo);
    		}
    		else{
    			$('#quantidade').val('1');
    		}
    	},

    	validarQuantidade: function(event){
    		var self = this;
    		var quantidade = $('#quantidade').val();
    		var multiplo = self.item.multiplo;
    		if(quantidade <= 0){
    			$('#titulo_erro').text('Quantidade Inválida');
    			$('#msg_erro').text('A quantidade deve ser maior que 0');
				$('#modal_erro').modal('show');
    		}
    		else{
    			if(multiplo){
    				if(quantidade % multiplo != 0){
    					$('#titulo_erro').text('Quantidade Inválida');
    					$('#msg_erro').text(`A quantidade deve ser multiplo de ${multiplo}. 
    					Exemplo: ${multiplo}, ${multiplo * 2}, ${multiplo * 3}, etc.`);
						$('#modal_erro').modal('show');
    				}
    			}
    		}
    	},

    	validarPreco: function(event){
    		var preco = decimal($('#preco').val());
    	},

    	addItem: function(event){
    		try{
	    		var self = this;
	    		var novo_item = [];
	    		novo_item.id = self.itens.length;
	    		novo_item.produto_id = self.item['id'];
	    		novo_item.nome = self.item['nome'];
	    		novo_item.quantidade = $('#quantidade').val();
	    		novo_item.preco = decimal($('#preco').val());
	    		novo_item.total = parseInt(novo_item.quantidade) * novo_item.preco;
	    		self.itens.push(novo_item);
    		} catch(err){
    			console.log(err);
    		}
    	}
    }
});

// configurações de ajustes no modal erro quantidade
// modal fechado
$('#modal_erro').on('hidden.bs.modal', function (e) {
  app.produtoSelecionado(e);
});

// modal aberto
$('#modal_erro').on('shown.bs.modal', function () {
  $('#btn_modal_fechar').trigger('focus');
})

// utils

// formato monetário
function dinheiro(value){
	var formato = { minimumFractionDigits: 2 , style: 'currency', currency: 'BRL' };
	return value.toLocaleString('pt-BR', formato);
}

// formato decimal
//Recebe um valor e retorna o float com 2 cadas decimais ou o valor passado.
function decimal(valor, precisao=2) {
    if (valor === null || valor === '' || valor === undefined)
        return null;
    valor = valor.replace('R$','').trim().replace(/\./g,'').replace(',','.');
    return parseFloat(valor).toFixed(precisao);
}