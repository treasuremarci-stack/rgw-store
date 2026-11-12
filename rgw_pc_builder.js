(()=>{'use strict';
const steps=[["Процессоры","Процессор"],["Материнские платы","Материнская плата"],["Оперативная память","Оперативная память"],["Видеокарты","Видеокарта"],["SSD","SSD"],["HDD","HDD"],["Корпуса","Корпус"],["Блоки питания","Блок питания"],["Охлаждение","Охлаждение"]];
const selected=new Map(),data=new Map(),root=document.getElementById('builderSteps'),summary=document.getElementById('builderSummary'),status=document.getElementById('builderStatus');
const facts=p=>[...(p.catalogFacts||[]),...(p.verifiedSpecs||[])];
const fact=(p,label)=>facts(p).find(f=>f.label.toLowerCase()===label.toLowerCase())?.value||'';
const norm=s=>String(s||'').toUpperCase().replace(/[\s-]/g,'');
const socket=p=>norm(fact(p,'Сокет'));
const ramType=p=>{const v=fact(p,'Тип памяти');return /DDR[345]/i.exec(v)?.[0]?.toUpperCase()||''};
const isLaptopRam=p=>/SO-DIMM|SODIMM|НОУТБУК/i.test(fact(p,'Форм-фактор')+' '+p.name);
function evaluate(p,category){
 const cpu=selected.get('Процессоры'),mb=selected.get('Материнские платы'),ram=selected.get('Оперативная память');
 if(category==='Материнские платы'&&cpu&&socket(cpu)&&socket(p)&&socket(cpu)!==socket(p))return {state:'bad',message:'Несовместимый сокет с процессором'};
 if(category==='Процессоры'&&mb&&socket(mb)&&socket(p)&&socket(mb)!==socket(p))return {state:'bad',message:'Несовместимый сокет с материнской платой'};
 if(category==='Оперативная память'&&isLaptopRam(p))return {state:'bad',message:'Ноутбучная память SO-DIMM'};
 if(category==='Оперативная память'&&mb&&ramType(p)&&ramType(mb)&&ramType(p)!==ramType(mb))return {state:'bad',message:'Тип памяти не подходит к плате'};
 if(category==='Материнские платы'&&ram&&ramType(p)&&ramType(ram)&&ramType(p)!==ramType(ram))return {state:'bad',message:'Тип памяти не подходит к выбранной ОЗУ'};
 return {state:'ok',message:''};
}
function make(tag,cls,txt){const e=document.createElement(tag);if(cls)e.className=cls;if(txt!==undefined)e.textContent=txt;return e}
function render(){
 root.replaceChildren();
 for(const [cat,title] of steps){const section=make('section','builder-step');const head=make('div','builder-step-head');head.append(make('h2','',title));const chosen=selected.get(cat);if(chosen){const clear=make('button','builder-clear','Убрать');clear.type='button';clear.addEventListener('click',()=>{selected.delete(cat);render()});head.append(clear)}section.append(head);
 const select=make('select','builder-select');select.setAttribute('aria-label','Выбрать: '+title);select.append(new Option('— Выберите '+title.toLowerCase()+' —',''));const items=data.get(cat)||[];for(const p of items){const check=evaluate(p,cat);const opt=new Option(p.name+(check.state==='bad'?' — '+check.message:''),p.id);opt.disabled=check.state==='bad';select.append(opt)}select.value=chosen?.id||'';select.addEventListener('change',()=>{const p=items.find(x=>x.id===select.value);if(p)selected.set(cat,p);else selected.delete(cat);render()});section.append(select);
 if(chosen){const detail=make('div','builder-chosen');if(chosen.image){const img=make('img');img.src=chosen.image;img.alt='';img.loading='lazy';detail.append(img)}const link=make('a','', 'Посмотреть товар →');link.href='product.html?id='+encodeURIComponent(chosen.id);detail.append(link);section.append(detail)}root.append(section)}
 const conflicts=[];const cpu=selected.get('Процессоры'),mb=selected.get('Материнские платы'),ram=selected.get('Оперативная память');
 if(cpu&&mb){if(socket(cpu)&&socket(mb)){if(socket(cpu)!==socket(mb))conflicts.push('Сокеты процессора и материнской платы не совпадают.');}else conflicts.push('Не удалось проверить сокет процессора или платы.');}
 if(mb&&ram){if(ramType(mb)&&ramType(ram)){if(ramType(mb)!==ramType(ram))conflicts.push('Тип ОЗУ не подходит к материнской плате.');}else conflicts.push('Не удалось подтвердить совместимость оперативной памяти.');}
 if(ram&&isLaptopRam(ram))conflicts.push('Выбрана ноутбучная память SO-DIMM.');
 summary.replaceChildren();for(const [cat,title] of steps){const row=make('div','builder-summary-row');row.append(make('span','',title),make('strong','',selected.get(cat)?.name||'Не выбран'));summary.append(row)}
 const n=selected.size;status.className=conflicts.some(x=>/не совпадают|не подходит|ноутбучная/.test(x))?'builder-status warning':'builder-status';status.textContent=conflicts.length?conflicts.join(' '):n?'Выбрано '+n+' из '+steps.length+' компонентов. Сокет CPU/платы и тип ОЗУ проверяются по данным каталога; BIOS, габариты, питание и охлаждение требуют дополнительной проверки.':'Выберите процессор и материнскую плату. Несовместимые варианты будут недоступны.';
 document.getElementById('builderReset').disabled=!n;
}
document.getElementById('builderReset').addEventListener('click',()=>{selected.clear();render()});
fetch('products.json').then(r=>{if(!r.ok)throw Error('Ошибка загрузки');return r.json()}).then(items=>{for(const [cat] of steps)data.set(cat,items.filter(p=>p.category===cat));render()}).catch(()=>{status.textContent='Не удалось загрузить каталог. Обновите страницу.';root.textContent='Список комплектующих временно недоступен.'});
})();