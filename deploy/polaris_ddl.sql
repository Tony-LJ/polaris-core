
---------------------------
-- 常用词汇中文映射表
---------------------------
drop table if exists utc.polaris_vocabulary_mapping;
create table if not exists utc.polaris_vocabulary_mapping (
    id INT AUTO_INCREMENT COMMENT 'id' ,
    field_cn varchar(50) default null COMMENT '中语字段',
    field_en varchar(50) default null COMMENT '英语字段',
    abbreviate varchar(50) default null COMMENT '字段缩写',
    descri varchar(200) default null COMMENT '字段描述',
    create_by varchar(64) default null comment '创建人',
    create_time datetime default current_timestamp comment '创建时间',
    update_by varchar(64) default null comment '更新人',
    update_time datetime default current_timestamp comment '更新时间',
    is_delete varchar(20) COMMENT '是否删除',
    remark varchar(200) COMMENT '备注',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT '常用词汇中文映射表'


