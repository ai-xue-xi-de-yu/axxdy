odoo.define('bicon_wms_base.bicon_list_view_button', function (require) {
    "use strict";
//这些是调⽤需要的模块
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    var ListController = require('web.ListController');
//    var assets_backend = require('web.assets_backend ')
//这块代码是继承ListController在原来的基础上进⾏扩展
    var BiConListController = ListController.extend({

        renderButtons: function () {
            this._super.apply(this, arguments);

            if (this.$buttons) {
                //这⾥找到刚才定义的class名为create_by_xf的按钮
                var btn = this.$buttons.find('.create_by_xf');
                //给按钮绑定click事件和⽅法create_data_by_dept
                btn.on('click', this.proxy('create_data_by_dept'));
            }
        },


        create_data_by_dept: function (instance) {
            //获取选中的记录
            var self = this;
            var records = _.map(self.selectedRecords, function (id) {
                return self.model.localData[id];
            });
            var ids = _.pluck(records, 'res_id');
            if(ids.length>1){
//            多条记录的批量操作
               this.do_action({
                        type: 'ir.actions.act_window',
                        res_model: "warehouse.warehouse",
                        view_mode: 'form',
                        view_type: 'form',
                        views: [[false, 'form']],
                        target: 'new',
                        context:{
                            ids :ids
                        },
                    })
            }else if(ids.length==1){
            this._rpc({
                    model :'material.examine',
                    method:'button_tree',
                    args:[ids],
                    }).then(function (result){
                    self.do_action(result)
                    })
            }else{
            alert('什么都没选呀')
            }
        },
    });
    var BiConListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: BiConListController,
        }),
    });

//这⾥⽤来注册编写的视图BiConListView，第⼀个字符串是注册名到时候需要根据注册名调⽤视图
    viewRegistry.add('bicon_list_view_button', BiConListView);
    return BiConListView;
});