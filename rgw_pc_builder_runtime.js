(()=>{'use strict';
const steps=[
  {key:'Процессоры',title:'Процессор',note:'Основа производительности сборки'},
  {key:'Материнские платы',title:'Материнская плата',note:'Сокет, чипсет и память'},
  {key:'Оперативная память',title:'Оперативная память',note:'Тип и объём памяти'},
  {key:'Видеокарты',title:'Видеокарта',note:'Графика и игры'},
  {key:'SSD',title:'SSD',note:'Быстрый системный накопитель'},
  {key:'HDD',title:'HDD',note:'Дополнительное хранилище'},
  {key:'Корпуса',title:'Корпус',note:'Форм-фактор и внешний вид'},
  {key:'Блоки питания',title:'Блок питания',note:'Питание компонентов'},
  {key:'Охлаждение',title:'Охлаждение',note:'Температура и шум'}
];
const state={selected:new Map(),data:new Map(),search:new Map(),onlyCompatible:false,active:steps[0].key};
const root=document.getElementById('builderSteps');
const status=document.getElementById('builderStatus');
const selectedCountNode=document.getElementById('builderSelectedCount');
const readyNote=document.getElementById('builderReadyNote');
const resetButton=document.getElementById('builderReset');
const copyButton=document.getElementById('builderCopy');
const modal=document.getElementById('builderModal');
const modalTitle=document.getElementById('builderModalTitle');
const modalNote=document.getElementById('builderModalNote');
const modalSearch=document.getElementById('builderSearch');
const modalCompatible=document.getElementById('builderCompatible');
const modalCount=document.getElementById('builderResultCount');
const modalGrid=document.getElementById('builderModalGrid');
const modalBack=document.getElementById('builderModalBack');
const modalClose=document.getElementById('builderModalClose');
let lastFocus=null;
const facts=product=>[...(product.catalogFacts||[]),...(product.verifiedSpecs||[])];
const fact=(product,label)=>facts(product).find(item=>String(item.label||'').toLowerCase()===label.toLowerCase())?.value||'';
const normalize=value=>String(value||'').toUpperCase().replace(/Ё/g,'Е').replace(/[^A-ZА-Я0-9]+/g,'');
const socket=product=>normalize(fact(product,'Сокет'));
const memoryType=product=>(/DDR[345]/i.exec(fact(product,'Тип памяти'))||[])[0]?.toUpperCase()||'';
const formFactor=product=>normalize(fact(product,'Форм-фактор'));
const laptopMemory=product=>/SO[- ]?DIMM|SODIMM|НОУТБУК/i.test(fact(product,'Форм-фактор')+' '+product.name);
function compatible(product,category){
  const cpu=state.selected.get('Процессоры');
  const board=state.selected.get('Материнские платы');
  const ram=state.selected.get('Оперативная память');
  if(category==='Материнские платы'&&cpu&&socket(cpu)&&socket(product)&&socket(cpu)!==socket(product))return{state:'bad',message:'Сокет не подходит к выбранному процессору'};
  if(category==='Процессоры'&&board&&socket(board)&&socket(product)&&socket(board)!==socket(product))return{state:'bad',message:'Сокет не подходит к выбранной плате'};
  if(category==='Оперативная память'&&laptopMemory(product))return{state:'bad',message:'Ноутбучная память SO-DIMM'};
  if(category==='Оперативная память'&&board&&memoryType(product)&&memoryType(board)&&memoryType(product)!==memoryType(board))return{state:'bad',message:'Тип памяти не подходит к выбранной плате'};
  if(category==='Материнские платы'&&ram&&memoryType(product)&&memoryType(ram)&&memoryType(product)!==memoryType(ram))return{state:'bad',message:'Тип памяти не подходит к выбранной ОЗУ'};
  const selectedCase=state.selected.get('Корпуса');
  if(category==='Материнские платы'&&selectedCase&&formFactor(product)&&formFactor(selectedCase)){
    const caseSize=formFactor(selectedCase),boardSize=formFactor(product);
    const supported=caseSize==='ATX'?['ATX','MICROATX','MINIITX'].includes(boardSize):caseSize==='MICROATX'?['MICROATX','MINIITX'].includes(boardSize):caseSize==='MINIITX'?boardSize==='MINIITX':true;
    if(!supported)return{state:'bad',message:'Материнская плата не помещается в выбранный корпус'};
  }
  if(category==='Корпуса'&&board&&formFactor(product)&&formFactor(board)){
    const caseSize=formFactor(product),boardSize=formFactor(board);
    const supported=caseSize==='ATX'?['ATX','MICROATX','MINIITX'].includes(boardSize):caseSize==='MICROATX'?['MICROATX','MINIITX'].includes(boardSize):caseSize==='MINIITX'?boardSize==='MINIITX':true;
    if(!supported)return{state:'bad',message:'Форм-фактор корпуса не подходит к плате'};
  }
  return{state:'ok',message:''};
}
function conflicts(){
  const messages=[];
  for(const step of steps){
    const product=state.selected.get(step.key);
    if(!product)continue;
    const result=compatible(product,step.key);
    if(result.state==='bad'&&!messages.includes(result.message))messages.push(result.message);
  }
  return messages;
}
function make(tag,className,text){
  const node=document.createElement(tag);
  if(className)node.className=className;
  if(text!==undefined)node.textContent=text;
  return node;
}
function factChips(product){
  return ['Сокет','Тип памяти','Форм-фактор','Мощность','Интерфейс','Объём'].map(label=>{
    const value=fact(product,label);
    return value?label+': '+value:'';
  }).filter(Boolean).slice(0,3);
}
function productMedia(product,className){
  const media=make('span',className||'builder-selector-media');
  if(product.image){
    const image=make('img');
    image.src=product.image;image.alt='';image.loading='lazy';image.decoding='async';
    media.append(image);
  }else media.textContent=product.placeholder||'🧩';
  return media;
}
function renderSelectedMedia(product){return productMedia(product,'builder-row-media')}
function renderRows(){
  root.replaceChildren();
  steps.forEach((step,index)=>{
    const product=state.selected.get(step.key);
    const row=make('article','builder-component-row'+(product?' is-selected':' builder-row-empty'));
    const main=make('div','builder-row-main');
    main.append(product?renderSelectedMedia(product):make('span','builder-row-media','+'+String(index+1)));
    const copy=make('div','builder-row-copy');
    copy.append(make('strong','',product?.name||step.title),make('span',product?'is-selected':'',product?factChips(product).join(' • '):step.note));
    main.append(copy);row.append(main);
    const actions=make('div','builder-row-actions');
    const choose=make('button','builder-row-button',product?'Изменить':'Добавить');
    choose.type='button';choose.setAttribute('aria-label',(product?'Изменить ':'Добавить ')+step.title);choose.addEventListener('click',()=>openChooser(step.key,choose));actions.append(choose);
    if(product){
      const remove=make('button','builder-row-remove','Удалить');remove.type='button';remove.addEventListener('click',()=>{state.selected.delete(step.key);renderRows();renderStatus()});actions.append(remove);
    }
    row.append(actions);root.append(row);
  });
}
function renderStatus(){
  const count=state.selected.size;const messages=conflicts();
  selectedCountNode.textContent=count+'/'+steps.length;readyNote.textContent='Выбрано '+count+' из '+steps.length;
  status.className='builder-status';
  if(messages.length){status.classList.add('warning');status.textContent='Проверьте сборку: '+messages.join('; ')+'.';readyNote.textContent+=' • есть предупреждение';}
  else if(count===0)status.textContent='Начните с процессора. Несовместимые варианты будут отмечены.';
  else if(count===steps.length)status.textContent='Все категории выбраны. Известные параметры сокета, памяти и форм-фактора проверены.';
  else{const next=steps.find(step=>!state.selected.has(step.key));status.textContent='Следующий шаг: '+(next?.title||'проверка сборки')+'. Несовместимые варианты будут недоступны.';}
  resetButton.disabled=count===0;
}
function render(){renderRows();renderStatus()}
function focusRowButton(key){
  const step=steps.find(item=>item.key===key);
  const button=step&&root.querySelector('button[aria-label="Изменить '+step.title+'"]');
  if(button)button.focus();
}
function closeChooser(){
  if(modal.hidden)return;
  modal.hidden=true;modal.setAttribute('aria-hidden','true');document.body.classList.remove('builder-modal-open');
  const target=lastFocus;lastFocus=null;if(target&&typeof target.focus==='function')target.focus();
}
function selectorCard(product,step){
  const check=compatible(product,step.key);const selected=state.selected.get(step.key)?.id===product.id;
  const card=make('article','builder-selector-card');card.classList.toggle('is-selected',selected);card.classList.toggle('is-disabled',check.state==='bad');
  card.append(productMedia(product,'builder-selector-media'));
  const content=make('div','builder-selector-content');
  content.append(make('span','builder-selector-brand',product.brand||step.title),make('strong','builder-selector-name',product.name));
  const factsNode=make('div','builder-selector-facts');for(const value of factChips(product))factsNode.append(make('span','',value));if(factsNode.childElementCount)content.append(factsNode);
  const button=make('button','builder-selector-button',selected?'Выбрано':check.state==='bad'?'Недоступно':'Добавить');button.type='button';button.disabled=check.state==='bad';button.setAttribute('aria-label',(selected?'Выбрано: ':check.state==='bad'?'Недоступно: ':'Добавить: ')+product.name);
  button.addEventListener('click',()=>{state.selected.set(step.key,product);closeChooser();render();focusRowButton(step.key)});content.append(button);card.append(content);
  const footer=make('div','builder-selector-footer');
  if(check.state==='bad')footer.append(make('span','builder-selector-reason',check.message));
  const link=make('a','builder-selector-link','Открыть карточку →');link.href='product.html?id='+encodeURIComponent(product.id);footer.append(link);card.append(footer);
  return card;
}
function renderChooser(){
  const step=steps.find(item=>item.key===state.active);if(!step)return;
  const all=state.data.get(step.key)||[];const query=normalize(state.search.get(step.key)||'');
  const items=all.filter(product=>{
    const text=normalize(product.name+' '+(product.brand||'')+' '+facts(product).map(item=>item.value).join(' '));
    const check=compatible(product,step.key);return(!query||text.includes(query))&&(!state.onlyCompatible||check.state!=='bad');
  });
  modalTitle.textContent=step.title;modalNote.textContent=step.note+' Выберите точную модель из каталога АКС.';modalCount.textContent=items.length+' из '+all.length+' вариантов';modalCompatible.checked=state.onlyCompatible;
  modalGrid.replaceChildren();items.forEach(product=>modalGrid.append(selectorCard(product,step)));
  if(!items.length)modalGrid.append(make('div','builder-empty',state.onlyCompatible?'Нет совместимых вариантов по текущим условиям.':'По вашему запросу ничего не найдено.'));
}
function openChooser(key,focusTarget){
  state.active=key;lastFocus=focusTarget||document.activeElement;modal.hidden=false;modal.setAttribute('aria-hidden','false');document.body.classList.add('builder-modal-open');
  modalSearch.value=state.search.get(key)||'';renderChooser();requestAnimationFrame(()=>modalSearch.focus());
}
function copyBuild(){
  const lines=['Сборка АКС'];
  steps.forEach(step=>{const product=state.selected.get(step.key);if(product)lines.push(step.title+': '+product.name)});
  const text=lines.join('\n');
  if(!navigator.clipboard?.writeText){copyButton.textContent='Скопируйте вручную';return;}
  navigator.clipboard.writeText(text).then(()=>{const previous=copyButton.textContent;copyButton.textContent='Скопировано';setTimeout(()=>{copyButton.textContent=previous},1400)}).catch(()=>{copyButton.textContent='Не удалось скопировать'});
}
function trapFocus(event){
  if(modal.hidden||event.key!=='Tab')return;
  const focusable=[...modal.querySelectorAll('button:not([disabled]),input:not([disabled]),a[href]')].filter(node=>node.offsetParent!==null);if(!focusable.length)return;
  const first=focusable[0],last=focusable[focusable.length-1];
  if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus()}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus()}
}
resetButton.addEventListener('click',()=>{state.selected.clear();state.search.clear();render()});
copyButton.addEventListener('click',copyBuild);
modalBack.addEventListener('click',closeChooser);modalClose.addEventListener('click',closeChooser);
modal.addEventListener('click',event=>{if(event.target===modal||event.target.matches('[data-builder-close]'))closeChooser()});
modalSearch.addEventListener('input',event=>{state.search.set(state.active,event.target.value);renderChooser()});
modalCompatible.addEventListener('change',event=>{state.onlyCompatible=event.target.checked;renderChooser()});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!modal.hidden)closeChooser();trapFocus(event)});
render();
fetch('products.json').then(response=>{if(!response.ok)throw new Error('products');return response.json()}).then(products=>{steps.forEach(step=>state.data.set(step.key,products.filter(product=>product.category===step.key)));render()}).catch(()=>{root.replaceChildren(make('div','builder-empty','Не удалось загрузить каталог. Обновите страницу.'));status.className='builder-status warning';status.textContent='Каталог временно недоступен.'});
})();
