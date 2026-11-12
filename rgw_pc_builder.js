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
const iconMarkup={
  'Процессоры':'<rect x="13" y="13" width="22" height="22" rx="3"/><rect x="19" y="19" width="10" height="10" rx="1"/><path d="M8 17h5M8 24h5M8 31h5M35 17h5M35 24h5M35 31h5M17 8v5M24 8v5M31 8v5M17 35v5M24 35v5M31 35v5"/>',
  'Материнские платы':'<rect x="8" y="7" width="32" height="34" rx="3"/><rect x="14" y="13" width="10" height="10" rx="1"/><path d="M28 13h7M28 18h7M14 29h21M14 34h21M28 23v6M34 23v6"/>',
  'Оперативная память':'<rect x="6" y="16" width="36" height="16" rx="3"/><path d="M12 20h4M19 20h4M26 20h4M33 20h3M10 32v5M15 32v5M20 32v5M25 32v5M30 32v5M35 32v5"/>',
  'Видеокарты':'<rect x="6" y="13" width="36" height="22" rx="3"/><circle cx="18" cy="24" r="6"/><circle cx="32" cy="24" r="6"/><path d="M6 18H3v12h3M42 20h3M42 28h3"/>',
  'SSD':'<rect x="8" y="14" width="32" height="20" rx="4"/><path d="M14 19h12M14 25h8M34 19h.1M34 25h.1M8 18H5v12h3"/>',
  'HDD':'<rect x="8" y="9" width="32" height="30" rx="5"/><circle cx="24" cy="24" r="8"/><circle cx="24" cy="24" r="2"/><path d="M24 16v6M17 31h14"/>',
  'Корпуса':'<rect x="14" y="6" width="20" height="36" rx="3"/><path d="M18 13h12M18 19h12M18 27h5M18 33h5"/><circle cx="29" cy="29" r="2"/>',
  'Блоки питания':'<rect x="6" y="10" width="36" height="28" rx="3"/><circle cx="18" cy="24" r="8"/><path d="M18 16v16M10 24h16M30 18h7M30 24h7M30 30h7"/>',
  'Охлаждение':'<circle cx="24" cy="24" r="15"/><circle cx="24" cy="24" r="3"/><path d="M24 21c-3-7 1-10 5-10 1 4-1 8-5 10ZM27 24c7-3 10 1 10 5-4 1-8-1-10-5ZM24 27c3 7-1 10-5 10-1-4 1-8 5-10ZM21 24c-7 3-10-1-10-5 4-1 8 1 10 5Z"/>'
};
const state={selected:new Map(),data:new Map(),search:new Map(),active:steps[0].key};
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

function reviewNeeded(product,category){
  const cpu=state.selected.get('Процессоры');
  const board=state.selected.get('Материнские платы');
  const ram=state.selected.get('Оперативная память');
  const selectedCase=state.selected.get('Корпуса');
  if((category==='Материнские платы'&&cpu||category==='Процессоры'&&board)&&(!socket(product)||!(category==='Процессоры'?socket(board):socket(cpu))))return'Сокет не указан — проверьте вручную';
  if((category==='Оперативная память'&&board||category==='Материнские платы'&&ram)&&(!memoryType(product)||!(category==='Оперативная память'?memoryType(board):memoryType(ram))))return'Тип памяти не указан — проверьте вручную';
  if((category==='Материнские платы'&&selectedCase||category==='Корпуса'&&board)&&(!formFactor(product)||!(category==='Корпуса'?formFactor(board):formFactor(selectedCase))))return'Форм-фактор не указан — проверьте вручную';
  return'';
}

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
  const review=reviewNeeded(product,category);
  if(review)return{state:'unknown',message:review};
  return{state:'ok',message:''};
}
function conflicts(){
  const messages=[];
  for(const step of steps){
    const product=state.selected.get(step.key);
    if(!product)continue;
    const result=compatible(product,step.key);
    if(result.state!=='ok'&&!messages.includes(result.message))messages.push(result.message);
  }
  return messages;
}
function make(tag,className,text){
  const node=document.createElement(tag);
  if(className)node.className=className;
  if(text!==undefined)node.textContent=text;
  return node;
}
function factChips(product,includeSocket=true){
  const labels=includeSocket?['Сокет','Тип памяти','Форм-фактор','Мощность','Интерфейс','Объём']:['Тип памяти','Форм-фактор','Мощность','Интерфейс','Объём'];
  return labels.map(label=>{
    const value=fact(product,label);
    return value?label+': '+value:'';
  }).filter(Boolean).slice(0,3);
}
function componentIcon(step){
  const icon=document.createElementNS('http://www.w3.org/2000/svg','svg');
  icon.setAttribute('class','builder-component-icon');icon.setAttribute('viewBox','0 0 48 48');icon.setAttribute('aria-hidden','true');icon.setAttribute('fill','none');icon.setAttribute('stroke','currentColor');icon.setAttribute('stroke-width','2.2');icon.setAttribute('stroke-linecap','round');icon.setAttribute('stroke-linejoin','round');icon.innerHTML=iconMarkup[step.key]||iconMarkup['Процессоры'];
  return icon;
}
function productMedia(product,className,step){
  const media=make('span',className||'builder-selector-media');
  if(product.image){
    const image=make('img');
    image.src=product.image;image.alt='';image.loading='lazy';image.decoding='async';
    media.append(image);
  }else media.append(componentIcon(step));
  return media;
}
function renderSelectedMedia(product,step){return productMedia(product,'builder-row-media',step)}
function renderRows(){
  root.replaceChildren();
  steps.forEach((step,index)=>{
    const product=state.selected.get(step.key);
    const row=make('article','builder-component-row'+(product?' is-selected':' builder-row-empty'));
    const main=make('div','builder-row-main');
    const media=product?renderSelectedMedia(product,step):make('span','builder-row-media');
    if(!product)media.append(componentIcon(step));
    main.append(media);
    const copy=make('div','builder-row-copy');
    copy.append(make('strong','',product?.name||step.title),make('span',product?'is-selected':'',product?factChips(product).join(' • '):step.note));
    main.append(copy);row.append(main);
    const actions=make('div','builder-row-actions');
    const choose=make('button','builder-row-button',product?'Изменить':'Добавить');
    choose.type='button';choose.setAttribute('aria-label',(product?'Изменить ':'Добавить ')+step.title);
    choose.addEventListener('click',()=>openChooser(step.key,choose));actions.append(choose);
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
  else if(count===0)status.textContent='Начните с процессора. Подтверждённо несовместимые варианты скрываются автоматически.';
  else if(count===steps.length)status.textContent='Все категории выбраны. Известные параметры сокета, памяти и форм-фактора проверены.';
  else{const next=steps.find(step=>!state.selected.has(step.key));status.textContent='Следующий шаг: '+(next?.title||'проверка сборки')+'. Подтверждённо несовместимые варианты скрываются автоматически.';}
  resetButton.disabled=count===0;
}
function render(){renderRows();renderStatus();}
function closeChooser(){
  if(modal.hidden)return;
  modal.hidden=true;modal.setAttribute('aria-hidden','true');document.body.classList.remove('builder-modal-open');
  const target=lastFocus;lastFocus=null;if(target&&typeof target.focus==='function')target.focus();
}
function selectorCard(product,step){
  const check=compatible(product,step.key);const selected=state.selected.get(step.key)?.id===product.id;
  const card=make('article','builder-selector-card');card.classList.toggle('is-selected',selected);card.classList.toggle('is-disabled',check.state==='bad');card.classList.toggle('is-review',check.state==='unknown');
  card.append(productMedia(product,'builder-selector-media',step));
  const content=make('div','builder-selector-content');
  content.append(make('span','builder-selector-brand',product.brand||step.title),make('strong','builder-selector-name',product.name));
  const factsNode=make('div','builder-selector-facts');for(const value of factChips(product,false))factsNode.append(make('span','',value));if(factsNode.childElementCount)content.append(factsNode);
  const button=make('button','builder-selector-button',selected?'Выбрано':check.state==='bad'?'Недоступно':'Добавить');button.type='button';button.disabled=check.state==='bad';button.setAttribute('aria-label',(selected?'Выбрано: ':check.state==='bad'?'Недоступно: ':'Добавить: ')+product.name);
  button.addEventListener('click',()=>{state.selected.set(step.key,product);closeChooser();render();});content.append(button);card.append(content);
  const footer=make('div','builder-selector-footer');
  if(check.state==='bad'||check.state==='unknown')footer.append(make('span',check.state==='unknown'?'builder-selector-review':'builder-selector-reason',check.message));
  const link=make('a','builder-selector-link','Открыть карточку →');link.href='product.html?id='+encodeURIComponent(product.id);footer.append(link);card.append(footer);
  return card;
}
function renderChooser(){
  const step=steps.find(item=>item.key===state.active);if(!step)return;
  const all=state.data.get(step.key)||[];const query=normalize(state.search.get(step.key)||'');
  const items=all.filter(product=>{
    const text=normalize(product.name+' '+(product.brand||'')+' '+facts(product).map(item=>item.value).join(' '));
    const check=compatible(product,step.key);return(!query||text.includes(query))&&check.state!=='bad';
  });
  modalTitle.textContent=step.title;modalNote.textContent=step.note+' Подтверждённо несовместимые варианты скрыты автоматически.';modalCount.textContent=items.length+' из '+all.length+' вариантов';
  modalGrid.replaceChildren();items.forEach(product=>modalGrid.append(selectorCard(product,step)));
  if(!items.length){const message=!all.length?'В этой категории пока нет товаров.':query?'По вашему запросу ничего не найдено.':'Нет совместимых вариантов по текущим условиям.';modalGrid.append(make('div','builder-empty',message));}
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
  navigator.clipboard.writeText(text).then(()=>{const previous=copyButton.textContent;copyButton.textContent='Скопировано';setTimeout(()=>{copyButton.textContent=previous},1400)}).catch(()=>{copyButton.textContent='Не удалось скопировать';});
}
function trapFocus(event){
  if(modal.hidden||event.key!=='Tab')return;
  const focusable=[...modal.querySelectorAll('button:not([disabled]),input:not([disabled]),a[href]')].filter(node=>node.offsetParent!==null);if(!focusable.length)return;
  const first=focusable[0],last=focusable[focusable.length-1];
  if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
}
document.getElementById('builderReset').addEventListener('click',()=>{state.selected.clear();state.search.clear();render()});
copyButton.addEventListener('click',copyBuild);
modalBack.addEventListener('click',closeChooser);modalClose.addEventListener('click',closeChooser);
modal.addEventListener('click',event=>{if(event.target===modal||event.target.matches('[data-builder-close]'))closeChooser()});
modalSearch.addEventListener('input',event=>{state.search.set(state.active,event.target.value);renderChooser()});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!modal.hidden)closeChooser();trapFocus(event)});
render();
fetch('products.json').then(response=>{if(!response.ok)throw new Error('products');return response.json()}).then(products=>{steps.forEach(step=>state.data.set(step.key,products.filter(product=>product.category===step.key)));render();}).catch(()=>{root.replaceChildren(make('div','builder-empty','Не удалось загрузить каталог. Обновите страницу.'));status.className='builder-status warning';status.textContent='Каталог временно недоступен.';});
})();
