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
const state={selected:new Map(),data:new Map(),prices:new Map(),search:new Map(),onlyCompatible:false,active:steps[0].key};
const root=document.getElementById('builderSteps');
const progress=document.getElementById('builderProgress');
const summary=document.getElementById('builderSummary');
const status=document.getElementById('builderStatus');
const totalNode=document.getElementById('builderTotal');
const priceNote=document.getElementById('builderPriceNote');
const selectedCountNode=document.getElementById('builderSelectedCount');
const readyNote=document.getElementById('builderReadyNote');
const resetButton=document.getElementById('builderReset');
const copyButton=document.getElementById('builderCopy');
const facts=p=>[...(p.catalogFacts||[]),...(p.verifiedSpecs||[])];
const fact=(p,label)=>facts(p).find(item=>String(item.label||'').toLowerCase()===label.toLowerCase())?.value||'';
const normalize=value=>String(value||'').toUpperCase().replace(/Ё/g,'Е').replace(/[^A-ZА-Я0-9]+/g,'');
const tokens=value=>String(value||'').toUpperCase().replace(/Ё/g,'Е').split(/[^A-ZА-Я0-9]+/).filter(Boolean);
const socket=p=>normalize(fact(p,'Сокет'));
const memoryType=p=>(/DDR[345]/i.exec(fact(p,'Тип памяти'))||[])[0]?.toUpperCase()||'';
const formFactor=p=>normalize(fact(p,'Форм-фактор'));
const laptopMemory=p=>/SO[- ]?DIMM|SODIMM|НОУТБУК/i.test(fact(p,'Форм-фактор')+' '+p.name);
const power=p=>{const match=String(fact(p,'Мощность')).match(/[0-9]+/);return match?Number(match[0]):null};
function parseSeparated(text){
  const rows=[];let row=[],field='',quoted=false;
  for(let i=0;i<text.length;i++){
    const char=text[i];
    if(char==='"'){
      if(quoted&&text[i+1]==='"'){field+='"';i++}else quoted=!quoted;
    }else if(char===';'&&!quoted){row.push(field);field=''}
    else if((char==='\n'||char==='\r')&&!quoted){
      if(char==='\r'&&text[i+1]==='\n')i++;
      row.push(field);field='';
      if(row.some(value=>String(value).trim()))rows.push(row);
      row=[];
    }else field+=char;
  }
  if(field||row.length){row.push(field);if(row.some(value=>String(value).trim()))rows.push(row)}
  return rows;
}
function loadPrices(text){
  for(const row of parseSeparated(text)){
    const name=String(row[0]||'').replace(/\s+/g,' ').trim();
    const raw=String(row[1]||'').trim();
    if(!name||!/^[0-9][0-9 ]*(?:[.,][0-9]+)?$/.test(raw))continue;
    const value=Number(raw.replace(/\s/g,'').replace(',','.'));
    if(Number.isFinite(value))state.prices.set(normalize(name),value);
  }
}
function priceFor(product){const value=state.prices.get(normalize(product.name));return Number.isFinite(value)?value:null}
function money(value){return '$'+new Intl.NumberFormat('en-US',{maximumFractionDigits:0}).format(value)}
function priceText(product){const value=priceFor(product);return value===null?'Цена уточняется':money(value)}
function compatible(product,category){
  const cpu=state.selected.get('Процессоры');
  const board=state.selected.get('Материнские платы');
  const ram=state.selected.get('Оперативная память');
  if(category==='Материнские платы'&&cpu&&socket(cpu)&&socket(product)&&socket(cpu)!==socket(product))return{state:'bad',message:'Сокет не подходит к выбранному процессору'};
  if(category==='Процессоры'&&board&&socket(board)&&socket(product)&&socket(board)!==socket(product))return{state:'bad',message:'Сокет не подходит к выбранной плате'};
  if(category==='Оперативная память'&&laptopMemory(product))return{state:'bad',message:'Ноутбучная память SO-DIMM'};
  if(category==='Оперативная память'&&board&&memoryType(product)&&memoryType(board)&&memoryType(product)!==memoryType(board))return{state:'bad',message:'Тип памяти не подходит к плате'};
  if(category==='Материнские платы'&&ram&&memoryType(product)&&memoryType(ram)&&memoryType(product)!==memoryType(ram))return{state:'bad',message:'Тип памяти не подходит к выбранной ОЗУ'};
  if(category==='Корпуса'&&board&&formFactor(product)&&formFactor(board)){
    const caseSize=formFactor(product);
    const boardSize=formFactor(board);
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
  const labels=['Сокет','Тип памяти','Форм-фактор','Мощность','Интерфейс','Объём'];
  return labels.map(label=>fact(product,label)).filter(Boolean).slice(0,3);
}
function productMedia(product,className){
  const media=make('span',className||'builder-card-media');
  if(product.image){
    const image=make('img');
    image.src=product.image;
    image.alt='';
    image.loading='lazy';
    image.decoding='async';
    media.append(image);
  }else media.textContent=product.placeholder||'🧩';
  return media;
}
function renderProgress(){
  progress.replaceChildren();
  steps.forEach((step,index)=>{
    const button=make('button','builder-progress-item');
    button.type='button';
    button.classList.toggle('is-active',state.active===step.key);
    button.classList.toggle('is-done',state.selected.has(step.key));
    button.setAttribute('role','tab');
    button.setAttribute('aria-selected',String(state.active===step.key));
    button.append(make('span','builder-progress-number',String(index+1)),make('span','builder-progress-label',step.title));
    button.addEventListener('click',()=>{state.active=step.key;render()});
    progress.append(button);
  });
}
function renderSelected(step,product){
  const row=make('div','builder-selected');
  row.append(productMedia(product,'builder-selected-media'));
  const copy=make('div','builder-selected-copy');
  copy.append(make('strong','',product.name),make('span','',priceText(product)));
  const link=make('a','', 'Открыть карточку →');
  link.href='product.html?id='+encodeURIComponent(product.id);
  copy.append(link);
  row.append(copy);
  return row;
}
function renderProductCard(product,step){
  const check=compatible(product,step.key);
  const selected=state.selected.get(step.key)?.id===product.id;
  const card=make('article','builder-product-card');
  card.classList.toggle('is-selected',selected);
  card.classList.toggle('is-disabled',check.state==='bad');
  const button=make('button','builder-card-button');
  button.type='button';
  button.disabled=check.state==='bad';
  button.setAttribute('aria-label',(selected?'Выбрано: ':'Добавить: ')+product.name);
  const content=make('span','builder-card-content');
  const top=make('span','builder-card-top');
  top.append(make('span','builder-card-brand',product.brand||step.title),make('span','builder-card-price',priceText(product)));
  content.append(top,make('span','builder-card-name',product.name));
  const factsNode=make('span','builder-card-facts');
  for(const value of factChips(product))factsNode.append(make('span','',value));
  if(factsNode.childElementCount)content.append(factsNode);
  content.append(make('span','builder-card-cta',selected?'Выбрано':'Добавить в сборку'));
  button.append(productMedia(product),content);
  button.addEventListener('click',()=>{
    if(check.state==='bad')return;
    state.selected.set(step.key,product);
    const next=steps.find((item,index)=>index>steps.findIndex(current=>current.key===step.key)&&!state.selected.has(item.key));
    state.active=next?.key||step.key;
    render();
  });
  card.append(button);
  const footer=make('div','builder-card-footer');
  if(check.state==='bad')footer.append(make('span','builder-card-reason',check.message));
  const link=make('a','builder-card-link','Подробнее →');
  link.href='product.html?id='+encodeURIComponent(product.id);
  footer.append(link);
  card.append(footer);
  return card;
}
function renderChooser(step,index){
  const chooser=make('div','builder-chooser');
  const toolbar=make('div','builder-chooser-toolbar');
  const input=make('input','builder-search');
  input.type='search';
  input.placeholder='Поиск по названию';
  input.value=state.search.get(step.key)||'';
  input.setAttribute('data-builder-search',String(index));
  input.setAttribute('aria-label','Поиск: '+step.title);
  input.addEventListener('input',event=>{state.search.set(step.key,event.target.value);render(index)});
  const label=make('label','builder-compatible');
  const checkbox=document.createElement('input');
  checkbox.type='checkbox';
  checkbox.checked=state.onlyCompatible;
  checkbox.addEventListener('change',event=>{state.onlyCompatible=event.target.checked;render()});
  label.append(checkbox,make('span','', 'Только совместимые'));
  toolbar.append(input,label);
  chooser.append(toolbar);
  const query=normalize(state.search.get(step.key)||'');
  let items=(state.data.get(step.key)||[]).filter(product=>{
    const searchable=normalize(product.name+' '+facts(product).map(item=>item.value).join(' '));
    const matches=!query||searchable.includes(query);
    const check=compatible(product,step.key);
    return matches&&(!state.onlyCompatible||check.state!=='bad');
  });
  const totalItems=(state.data.get(step.key)||[]).length;
  chooser.append(make('div','builder-result-count',items.length+' из '+totalItems+' вариантов'));
  const grid=make('div','builder-product-grid');
  items.forEach(product=>grid.append(renderProductCard(product,step)));
  if(!items.length){
    const empty=make('div','builder-empty',state.onlyCompatible?'Нет совместимых вариантов по текущим условиям.':'По вашему запросу ничего не найдено.');
    empty.style.gridColumn='1 / -1';
    grid.append(empty);
  }
  chooser.append(grid);
  return chooser;
}
function renderStep(step,index){
  const section=make('section','builder-step');
  section.classList.toggle('is-active',state.active===step.key);
  const head=make('div','builder-step-head');
  const toggle=make('button','builder-step-toggle');
  toggle.type='button';
  toggle.setAttribute('aria-expanded',String(state.active===step.key));
  const number=make('span','builder-step-number',String(index+1));
  const copy=make('span','builder-step-copy');
  copy.append(make('span','builder-step-title',step.title),make('span','builder-step-subtitle',state.selected.get(step.key)?.name||step.note));
  const stateLabel=make('span','builder-step-state',state.selected.has(step.key)?'Выбрано':'Не выбрано');
  stateLabel.classList.toggle('is-selected',state.selected.has(step.key));
  toggle.append(number,copy,stateLabel);
  toggle.addEventListener('click',()=>{state.active=step.key;render()});
  head.append(toggle);
  const product=state.selected.get(step.key);
  if(product){
    const clear=make('button','builder-clear','Убрать');
    clear.type='button';
    clear.addEventListener('click',()=>{state.selected.delete(step.key);state.active=step.key;render()});
    head.append(clear);
  }
  section.append(head);
  if(product)section.append(renderSelected(step,product));
  if(state.active===step.key)section.append(renderChooser(step,index));
  return section;
}
function renderSummary(){
  summary.replaceChildren();
  let total=0;let unknown=0;
  steps.forEach(step=>{
    const row=make('div','builder-summary-row');
    const jump=make('button','builder-summary-jump');
    jump.type='button';
    jump.addEventListener('click',()=>{state.active=step.key;render()});
    const product=state.selected.get(step.key);
    if(product){
      jump.append(make('span','',step.title),make('strong','',product.name));
      const value=priceFor(product);
      if(value===null){unknown++}
      row.append(jump,make('span','builder-summary-price',priceText(product)));
    }else{
      jump.append(make('span','',step.title),make('strong','builder-summary-empty','Не выбран'));
      row.append(jump);
    }
    summary.append(row);
    if(product&&priceFor(product)!==null)total+=priceFor(product);
  });
  const count=state.selected.size;
  selectedCountNode.textContent=count+'/'+steps.length;
  totalNode.textContent=count===0?'$0':total?money(total):'Уточняется';
  priceNote.textContent=unknown?'Для '+unknown+' позиции цена уточняется':'Цены берутся из price.csv';
}
function renderStatus(){
  const messages=conflicts();
  const count=state.selected.size;
  status.className='builder-status';
  if(messages.length){
    status.classList.add('warning');
    status.textContent='Проверьте сборку: '+messages.join('; ')+'.';
  }else if(count===0){
    status.textContent='Начните с процессора. Несовместимые варианты будут недоступны.';
  }else if(count===steps.length){
    status.textContent='Все компоненты выбраны. Базовые проверки совместимости пройдены.';
  }else{
    const next=steps.find(step=>!state.selected.has(step.key));
    status.textContent='Выбрано '+count+' из '+steps.length+'. Следующий шаг: '+(next?.title||'проверка сборки')+'.';
  }
  resetButton.disabled=count===0;
  readyNote.textContent='Выбрано '+count+' из '+steps.length+(messages.length?' • есть предупреждение':'');
}
function render(focusIndex=null){
  renderProgress();
  root.replaceChildren();
  steps.forEach((step,index)=>root.append(renderStep(step,index)));
  renderSummary();
  renderStatus();
  if(focusIndex!==null){
    const input=document.querySelector('[data-builder-search="'+focusIndex+'"]');
    if(input){input.focus();input.setSelectionRange(input.value.length,input.value.length)}
  }
}
function copyBuild(){
  const lines=['Сборка АКС'];
  steps.forEach(step=>{const product=state.selected.get(step.key);if(product)lines.push(step.title+': '+product.name+' — '+priceText(product))});
  lines.push('Итого: '+totalNode.textContent);
  const text=lines.join('\n');
  if(!navigator.clipboard?.writeText){copyButton.textContent='Скопируйте вручную';return}
  navigator.clipboard.writeText(text).then(()=>{
    const previous=copyButton.textContent;
    copyButton.textContent='Скопировано';
    setTimeout(()=>{copyButton.textContent=previous},1400);
  }).catch(()=>{copyButton.textContent='Не удалось скопировать';});
}
resetButton.addEventListener('click',()=>{state.selected.clear();state.search.clear();state.active=steps[0].key;render()});
copyButton.addEventListener('click',copyBuild);
render();
Promise.all([
  fetch('products.json').then(response=>{if(!response.ok)throw new Error('products');return response.json()}),
  fetch('price.csv').then(response=>{if(!response.ok)throw new Error('price');return response.text()})
]).then(([products,priceCsv])=>{
  loadPrices(priceCsv);
  steps.forEach(step=>state.data.set(step.key,products.filter(product=>product.category===step.key)));
  render();
}).catch(()=>{
  root.replaceChildren(make('div','builder-empty','Не удалось загрузить каталог. Обновите страницу.'));
  status.className='builder-status warning';
  status.textContent='Каталог временно недоступен.';
});
})();