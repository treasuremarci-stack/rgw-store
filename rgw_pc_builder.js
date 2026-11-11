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
 const picker=make('div','builder-picker');const open=make('button','builder-pick-button',chosen?'Заменить компонент':'Выбрать компонент');open.type='button';open.setAttribute('aria-expanded','false');picker.append(open);const panel=make('div','builder-options');panel.hidden=true;const search=make('input','builder-search');search.type='search';search.placeholder='Поиск по названию';search.setAttribute('aria-label','Поиск: '+title);panel.append(search);const list=make('div','builder-option-list');panel.append(list);function populate(){list.replaceChildren();let count=0;for(const p of data.get(cat)||[]){if(!p.name.toLowerCase().includes(search.value.trim().toLowerCase()))continue;count++;const check=evaluate(p,cat),btn=make('button','builder-option'+(check.state==='bad'?' incompatible':''));btn.type='button';btn.disabled=check.state==='bad';if(p.image){const img=make('img','builder-option-img');img.src=p.image;img.alt='';img.loading='lazy';btn.append(img)}const copy=make('span','builder-option-copy');copy.append(make('strong','',p.name));if(check.state==='bad')copy.append(make('small','',check.message));else{const info=[fact(p,'Сокет'),fact(p,'Тип памяти'),fact(p,'Форм-фактор')].filter(Boolean).slice(0,2).join(' · ');if(info)copy.append(make('small','',info))}btn.append(copy);btn.addEventListener('click',()=>{selected.set(cat,p);render()});list.append(btn)}if(!count)list.append(make('p','builder-empty','По запросу ничего не найдено'))}open.addEventListener('click',()=>{panel.hidden=!panel.hidden;open.setAttribute('aria-expanded',String(!panel.hidden));if(!panel.hidden){populate();search.focus()}});search.addEventListener('input',populate);section.append(picker);picker.append(panel);
 if(chosen){const detail=make('div','builder-chosen');if(chosen.image){const img=make('img');img.src=chosen.image;img.alt='';img.loading='lazy';detail.append(img)}const name=make('div','builder-chosen-name');name.append(make('strong','',chosen.name));const link=make('a','', 'Посмотреть товар →');link.href='product.html?id='+encodeURIComponent(chosen.id);name.append(link);detail.append(name);section.append(detail)}root.append(section)}
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