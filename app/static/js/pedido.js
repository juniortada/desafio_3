// Author: Junior Tada

Vue.prototype.axios = window.axios;

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
	        valJson = $('#pedidoJson').val();
	        if(valJson !== ''){
	        	var editarJson = JSON.parse(valJson);
	        	this.carregarPedido(editarJson);
	        }
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

    	carregarPedido: function(json){
    		var self = this;
    		self.cliente = json['cliente'];
    		for(i in json['itens']){
    			var novo_item = [];
	    		novo_item.id = self.itens.length;
	    		novo_item.produto_id = json.itens[i].produto_id;
	    		novo_item.nome = json.itens[i].nome;
	    		novo_item.quantidade = json.itens[i].quantidade;
	    		novo_item.preco = json.itens[i].preco
	    		novo_item.total = json.itens[i].total
	    		novo_item.rentabilidade = json.itens[i].rentabilidade
	    		self.itens.push(novo_item);
    		}
    	},

    	produtoSelecionado: function(event){
    		var self = this;
    		self.item = self.produtos[self.produto -1];
    		if(self.item !== undefined){
	    		// set preço
	    		$('#preco').val(dinheiro(self.item.preco));
	    		// valida e set multiplo
	    		if(self.item.multiplo){
	    			$('#quantidade').val(self.item.multiplo);
	    		}
	    		else{
	    			$('#quantidade').val('1');
	    		}
	    		self.validarPreco();
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
    			if(multiplo && (quantidade % multiplo != 0)){
					$('#titulo_erro').text('Quantidade Inválida');
					$('#msg_erro').text(`A quantidade deve ser multiplo de ${multiplo}. 
					Exemplo: ${multiplo}, ${multiplo * 2}, ${multiplo * 3}, etc.`);
					$('#modal_erro').modal('show');
    			}
    		}
    	},

    	validarPreco: function(event){
    		var self = this;
    		var preco = decimal($('#preco').val());
    		if(preco === null || preco <= 0){
    			$('#titulo_erro').text('Preço Inválido');
    			$('#msg_erro').text('O preço deve ser maior que 0 e um valor válido!');
    			$('#modal_erro').modal('show');
    		}
    		else{
    			if(preco > self.item['preco']){
    				self.item.rentabilidade = 'Ótima';
    				$('#rentabilidade').text('Ótima');
    				self.item.rentabilidade = 'Ótima';
    			}
    			else{
    				if((preco === self.item['preco']) || preco >= porcentagem(self.item['preco'])){
    					$('#rentabilidade').text('Boa');
    					self.item.rentabilidade = 'Boa';
    				}
    				else{
    					$('#rentabilidade').text('Ruim');
    					$('#titulo_erro').text('Rentabilidade Ruim');
		    			$('#msg_erro').text('O preço deve ser no máximo 10% abaixo!');
		    			$('#modal_erro').modal('show');
    				}
    			}
    		}
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
	    		novo_item.total = parseFloat(parseInt(novo_item.quantidade) * novo_item.preco).toFixed(2);
	    		novo_item.rentabilidade = self.item['rentabilidade'];
	    		self.itens.push(novo_item);
    		} catch(err){
    			console.log(err);
    		}
    	},

    	submit: function(event){
    		try{
    			var self = this;
    			// valida cliente
    			if(self.cliente === '' || self.cliente === null){
    				$('#titulo_erro').text('Escolha um Cliente');
	    			$('#msg_erro').text('Nenhum cliente selecionado, por favor escolha um cliente!');
	    			$('#modal_erro').modal('show');
    			}
				else{
					// valida itens
					if(self.itens.length <= 0){
						$('#titulo_erro').text('Escolha Algum Item');
		    			$('#msg_erro').text('Nenhum item selecionado, por favor escolha um item!');
		    			$('#modal_erro').modal('show');
					}
					else{
						// transforma lista de itens em objetos serializaveis
						var itens = {};
						for(i in self.itens){
							obj = Object.assign({}, self.itens[i]);
							itens[obj['id']] = obj;
						}
						pedidos = JSON.stringify({
							cliente: self.cliente, 
							itens: itens});
						$('#pedidoJson').val(pedidos);
						$('#form_pedido').submit();
					}
				}
    		}
    		catch(err){
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

// porcentagem
function porcentagem(preco){
	return (preco - ((preco/100) * 10))
}