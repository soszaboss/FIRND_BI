// Imports
import { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { CKEditor } from '@ckeditor/ckeditor5-react';
import {
	ClassicEditor,
	AccessibilityHelp,
	Alignment,
	Autoformat,
	AutoImage,
	AutoLink,
	Autosave,
	BlockQuote,
	Bold,
	CKBox,
	CKBoxImageEdit,
	CloudServices,
	Code,
	Essentials,
	FindAndReplace,
	FontBackgroundColor,
	FontColor,
	FontFamily,
	FontSize,
	GeneralHtmlSupport,
	Heading,
	Highlight,
	HorizontalLine,
	ImageBlock,
	ImageCaption,
	ImageInline,
	ImageInsert,
	ImageInsertViaUrl,
	ImageResize,
	ImageStyle,
	ImageTextAlternative,
	ImageToolbar,
	ImageUpload,
	Indent,
	IndentBlock,
	Italic,
	Link,
	LinkImage,
	List,
	ListProperties,
	Mention,
	PageBreak,
	Paragraph,
	PasteFromOffice,
	PictureEditing,
	RemoveFormat,
	SelectAll,
	SourceEditing,
	SpecialCharacters,
	SpecialCharactersArrows,
	SpecialCharactersCurrency,
	SpecialCharactersEssentials,
	SpecialCharactersLatin,
	SpecialCharactersMathematical,
	SpecialCharactersText,
	Strikethrough,
	Style,
	Subscript,
	Superscript,
	Table,
	TableCaption,
	TableCellProperties,
	TableColumnResize,
	TableProperties,
	TableToolbar,
	TextTransformation,
	TodoList,
	Underline,
	Undo
} from 'ckeditor5';
import {
	CaseChange,
	ExportPdf,
	ExportWord,
	FormatPainter,
	ImportWord,
	MergeFields,
	MultiLevelList,
	PasteFromOfficeEnhanced,
	SlashCommand,
	TableOfContents,
	Template
} from 'ckeditor5-premium-features';
import axios from 'axios';
import styled from 'styled-components';
import ViewDiploma from './components/ViewDiploma';

// Styles
import 'ckeditor5/ckeditor5.css';
import 'ckeditor5-premium-features/ckeditor5-premium-features.css';
import './App.css';

// Constants
const LICENSE_KEY = 'Q3hqUW1RS1NVSTM2UExMcytPMnUzWk1kcmxEMUw4UVVtNFFnUVZkdWhramtjN1hRbFVkS3ZlT0N0KzlSbmc9PS1NakF5TkRBNU1qaz0=';
const CKBOX_TOKEN_URL = 'https://117321.cke-cs.com/token/dev/Ap04no6ko1MvNnf1wH33Dnwd1Haue2vPKVlr?limit=10';

// Define template options
const templates = [
  { name: 'BTS', file: 'bts-template.txt' },
  { name: 'BT', file: 'bt-template.txt' },
  { name: 'BEP', file: 'bep-template.txt' },
  { name: 'CAP', file: 'cap-template.txt' },
  { name: 'BP', file: 'bp-template.txt' },
];

// New function to fetch custom data
const fetchCustomData = async (templateFile) => {
  try {
    const [templateResponse, dataResponse] = await Promise.all([
      axios.get(`/${templateFile}`),
      axios.get(`/mockData/${templateFile.replace('template.txt', 'data.json')}`)
    ]);
    return {
      templateData: templateResponse.data,
      dataSets: dataResponse.data.dataSets
    };
  } catch (error) {
    console.error('Error fetching custom data:', error);
    return {
      templateData: '<p>Failed to load custom data. Please try again later.</p>',
      dataSets: []
    };
  }
};

// Styled components for the menu
const MenuBar = styled.nav`
  background-color: #5DBE9D;
  padding: 10px 20px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
`;

const MenuButton = styled.button`
  background-color: transparent;
  border: none;
  color: white;
  font-size: 16px;
  cursor: pointer;
  padding: 10px 15px;
  margin-left: 20px;
  transition: background-color 0.3s;

  &:hover {
    background-color: rgba(255, 255, 255, 0.2);
  }
`;

const DropdownContent = styled.div`
  display: ${props => props.show ? 'block' : 'none'};
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1001; // Ensure it's above other elements
`;

const DropdownItem = styled.button`
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  cursor: pointer;
  background-color: transparent;
  border: none;
  width: 100%;
  text-align: left;

  &:hover {
    background-color: #f1f1f1;
  }
`;

// Add this new component for merge field selection
const MergeFieldSelector = styled.div`
  padding: 10px;
`;

// Define merge fields for each template type
const mergeFieldDefinitions = {
  bts: [
    { id: 'Nom_etudiant', label: 'Nom de l\'étudiant', defaultValue: '' },
    { id: 'specialite', label: 'Spécialité', defaultValue: '' },
    { id: 'Date', label: 'Date de délivrance', defaultValue: '' },
    { id: 'Signature', label: 'Signature', defaultValue: '' }
  ],
  bt: [
    { id: 'Nom_etudiant', label: 'Nom de l\'étudiant', defaultValue: '' },
    { id: 'specialite', label: 'Spécialité', defaultValue: '' },
    { id: 'Date', label: 'Date de délivrance', defaultValue: '' },
    { id: 'Signature', label: 'Signature', defaultValue: '' }
  ],
  bep: [
    { id: 'Nom_etudiant', label: 'Nom de l\'étudiant', defaultValue: '' },
    { id: 'specialite', label: 'Spécialité', defaultValue: '' },
    { id: 'Date', label: 'Date de délivrance', defaultValue: '' },
    { id: 'Signature', label: 'Signature', defaultValue: '' }
  ],
  cap: [
    { id: 'Nom_etudiant', label: 'Nom de l\'étudiant', defaultValue: '' },
    { id: 'specialite', label: 'Spécialité', defaultValue: '' },
    { id: 'date', label: 'Date de délivrance', defaultValue: '' },
    { id: 'signature', label: 'Signature', defaultValue: '' }
  ],
  bp: [
    { id: 'Nom_etudiant', label: 'Nom de l\'étudiant', defaultValue: '' },
    { id: 'specialite', label: 'Spécialité', defaultValue: '' },
    { id: 'Date', label: 'Date de délivrance', defaultValue: '' },
    { id: 'Signature', label: 'Signature', defaultValue: '' }
  ]
};

// Update the styled component for the main container
const MainContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f0f0f0;
  min-height: calc(100vh - 60px); // Adjust based on your MenuBar height
`;

const EditorWrapper = styled.div`
  width: 100%;
  max-width: 1200px;
  margin: 20px auto;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  overflow: hidden;
`;

const EditorHeader = styled.div`
  background-color: #f5f5f5;
  padding: 15px;
  border-bottom: 1px solid #e0e0e0;
`;

const EditorContent = styled.div`
  padding: 20px;
`;

// Main App component
export default function App() {
	const editorContainerRef = useRef(null);
	const editorRef = useRef(null);
	const [isLayoutReady, setIsLayoutReady] = useState(false);
	const [initialData, setInitialData] = useState('');
	const [selectedTemplate, setSelectedTemplate] = useState(null);
	const [showTemplates, setShowTemplates] = useState(false);
	const [showModal, setShowModal] = useState(false);
	const [mergeFieldValues, setMergeFieldValues] = useState({});
	const [dataSets, setDataSets] = useState([]);
	const [currentDataSet, setCurrentDataSet] = useState(null);
  const [currentMergeFields, setCurrentMergeFields] = useState([]);
  const [availableDataSets, setAvailableDataSets] = useState([]);
  const [isCustomData, setIsCustomData] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

	useEffect(() => {
		// Initialize merge field values with default values
		const initialValues = {};
		//mergeFieldDefinitions.forEach(field => {
			//initialValues[field.id] = field.defaultValue;
		//});
		//setMergeFieldValues(initialValues);
	}, []);

	// Update loadCustomData function
	const loadCustomData = useCallback(async (templateFile) => {
    setIsLoading(true);
    try {
      const { templateData, dataSets } = await fetchCustomData(templateFile);
      setInitialData(templateData);
      setDataSets(dataSets);
      setAvailableDataSets(dataSets);
      
      const templateType = templateFile.split('-')[0];
      const newMergeFields = mergeFieldDefinitions[templateType];
      setCurrentMergeFields(newMergeFields);

      if (dataSets.length > 0) {
        setCurrentDataSet(dataSets[0]);
        setMergeFieldValues(dataSets[0].values);
      } else {
        setCurrentDataSet(null);
        setMergeFieldValues({});
      }

      // Update the editor content
      if (editorRef.current && editorRef.current.editor) {
        editorRef.current.editor.setData(templateData);
      }
    } catch (error) {
      console.error('Error loading custom data:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

	useEffect(() => {
		// Check if layout is ready
		setIsLayoutReady(true);
		return () => setIsLayoutReady(false);
	}, []);

	// Ensure initial data is set correctly
	useEffect(() => {
		if (initialData) {
			// Check if editor is ready to set data
			if (editorRef.current && editorRef.current.editor) {
				editorRef.current.editor.setData(initialData);
			}
		}
	}, [initialData]);

	useEffect(() => {
		if (selectedTemplate) {
			const templateType = selectedTemplate.split('-')[0];
			setCurrentMergeFields(mergeFieldDefinitions[templateType]);
			// Reset mergeFieldValues when changing templates
			setMergeFieldValues({});
			loadCustomData(selectedTemplate);
		}
	}, [selectedTemplate]);

	// Editor configuration
	const editorConfig = useMemo(() => {
		if (!selectedTemplate) return {}; // Prevents using null selectedTemplate

		return {
			toolbar: {
				items: [
					'undo', 'redo', '|',
					'insertMergeField', 'previewMergeFields', '|',
					'sourceEditing', 'importWord', 'exportWord', 'exportPdf', 'formatPainter', 'caseChange', 'findAndReplace', 'selectAll', '|',
					'heading', 'style', '|',
					'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', '|',
					'bold', 'italic', 'underline', 'strikethrough', 'subscript', 'superscript', 'code', 'removeFormat', '|',
					'specialCharacters', 'horizontalLine', 'pageBreak', 'link', 'insertImage', 'insertImageViaUrl', 'ckbox', 'insertTable', 'tableOfContents', 'insertTemplate', 'highlight', 'blockQuote', '|',
					'alignment', '|',
					'bulletedList', 'numberedList', 'multiLevelList', 'todoList', 'outdent', 'indent', '|',
					'accessibilityHelp'
				],
				shouldNotGroupWhenFull: false
			},
			plugins: [
				AccessibilityHelp, Alignment, Autoformat, AutoImage, AutoLink, Autosave, BlockQuote, Bold, CaseChange, CKBox, CKBoxImageEdit, CloudServices, Code,
				 Essentials, ExportPdf, ExportWord, FindAndReplace, FontBackgroundColor, FontColor, FontFamily, FontSize, FormatPainter, GeneralHtmlSupport, Heading,
				  Highlight, HorizontalLine, ImageBlock, ImageCaption, ImageInline, ImageInsert, ImageInsertViaUrl, ImageResize, ImageStyle, ImageTextAlternative,
				   ImageToolbar, ImageUpload, ImportWord, Indent, IndentBlock, Italic, Link, LinkImage, List, ListProperties, Mention, MergeFields, MultiLevelList,
				    PageBreak, Paragraph, PasteFromOffice, PasteFromOfficeEnhanced, PictureEditing, RemoveFormat, SelectAll, SlashCommand, SourceEditing,
					 SpecialCharacters, SpecialCharactersArrows, SpecialCharactersCurrency, SpecialCharactersEssentials, SpecialCharactersLatin,
					  SpecialCharactersMathematical, SpecialCharactersText, Strikethrough, Style, Subscript, Superscript, Table, TableCaption, TableCellProperties,
					   TableColumnResize, TableOfContents, TableProperties, TableToolbar, Template, TextTransformation, TodoList, Underline, Undo
			],
			ckbox: {
				tokenUrl: CKBOX_TOKEN_URL
			},
			exportPdf: {
				stylesheets: [
					/* This path should point to application stylesheets. */
					/* See: https://ckeditor.com/docs/ckeditor5/latest/features/converters/export-pdf.html */
					'./App.css',
					/* Export PDF needs access to stylesheets that style the content. */
					'https://cdn.ckeditor.com/ckeditor5/43.0.0/ckeditor5.css',
					'https://cdn.ckeditor.com/ckeditor5-premium-features/43.0.0/ckeditor5-premium-features.css'
				],
				fileName: `${selectedTemplate.split('-')[0]}-template.pdf`,
				converterOptions: {
					format: 'Tabloid',
					margin_top: '20mm',
					margin_bottom: '20mm',
					margin_right: '24mm',
					margin_left: '24mm',
					page_orientation: 'portrait'
				}
			},
			exportWord: {
				stylesheets: [
					/* This path should point to application stylesheets. */
					/* See: https://ckeditor.com/docs/ckeditor5/latest/features/converters/export-word.html */
					'./App.css',
					/* Export Word needs access to stylesheets that style the content. */
					'https://cdn.ckeditor.com/ckeditor5/43.0.0/ckeditor5.css',
					'https://cdn.ckeditor.com/ckeditor5-premium-features/43.0.0/ckeditor5-premium-features.css'
				],
				fileName: `${selectedTemplate.split('-')[0]}-template.docx`,
				converterOptions: {
					document: {
						size: 'Tabloid',
						margins: {
							top: '20mm',
							bottom: '20mm',
							right: '24mm',
							left: '24mm',
							page_orientation: 'portrait'
						}
					}
				}
			},
			fontFamily: {
				supportAllValues: true
			},
			fontSize: {
				options: [10, 12, 14, 'default', 18, 20, 22],
				supportAllValues: true
			},
			heading: {
				options: [
					{
						model: 'paragraph',
						title: 'Paragraph',
						class: 'ck-heading_paragraph'
					},
					{
						model: 'heading1',
						view: 'h1',
						title: 'Heading 1',
						class: 'ck-heading_heading1'
					},
					{
						model: 'heading2',
						view: 'h2',
						title: 'Heading 2',
						class: 'ck-heading_heading2'
					},
					{
						model: 'heading3',
						view: 'h3',
						title: 'Heading 3',
						class: 'ck-heading_heading3'
					},
					{
						model: 'heading4',
						view: 'h4',
						title: 'Heading 4',
						class: 'ck-heading_heading4'
					},
					{
						model: 'heading5',
						view: 'h5',
						title: 'Heading 5',
						class: 'ck-heading_heading5'
					},
					{
						model: 'heading6',
						view: 'h6',
						title: 'Heading 6',
						class: 'ck-heading_heading6'
					}
				]
			},
			htmlSupport: {
				allow: [
					{
						name: /^.*$/,
						styles: true,
						attributes: true,
						classes: true
					}
				]
			},
			image: {
				toolbar: [
					'toggleImageCaption',	'imageTextAlternative',	'|',
					'imageStyle:inline',	'imageStyle:wrapText',
					'imageStyle:breakText',	'|',
					'resizeImage',
					'|',
					'ckboxImageEdit'
				]
			},
			initialData: initialData,
			licenseKey: LICENSE_KEY,
			link: {
				addTargetToExternalLinks: true,
				defaultProtocol: 'https://',
				decorators: {
					toggleDownloadable: {
						mode: 'manual',
						label: 'Downloadable',
						attributes: {
							download: 'file'
						}
					}
				}
			},
			list: {
				properties: {
					styles: true,
					startIndex: true,
					reversed: true
				}
			},
			mention: {
				feeds: [
					{
						marker: '@',
						feed: [
							/* See: https://ckeditor.com/docs/ckeditor5/latest/features/mentions.html */
						]
					}
				]
			},
			menuBar: {
				isVisible: true
			},
			mergeFields: {
				definitions: currentMergeFields,
				dataSets: dataSets,
				previewMode: '$dataSets',
			},
			placeholder: 'Type or paste your content here!',
			style: {
				definitions: [
					{
						name: 'Article category',
						element: 'h3',
						classes: ['category']
					},
					{
						name: 'Title',
						element: 'h2',
						classes: ['document-title']
					},
					{
						name: 'Subtitle',
						element: 'h3',
						classes: ['document-subtitle']
					},
					{
						name: 'Info box',
						element: 'p',
						classes: ['info-box']
					},
					{
						name: 'Side quote',
						element: 'blockquote',
						classes: ['side-quote']
					},
					{
						name: 'Marker',
						element: 'span',
						classes: ['marker']
					},
					{
						name: 'Spoiler',
						element: 'span',
						classes: ['spoiler']
					},
					{
						name: 'Code (dark)',
						element: 'pre',
						classes: ['fancy-code', 'fancy-code-dark']
					},
					{
						name: 'Code (bright)',
						element: 'pre',
						classes: ['fancy-code', 'fancy-code-bright']
					}
				]
			},
			table: {
				contentToolbar: ['tableColumn', 'tableRow', 'mergeTableCells', 'tableProperties', 'tableCellProperties']
			},
			template: {
				definitions: [
					{
						title: 'Introduction',
						description: 'Simple introduction to an article',
						icon: '<svg width="45" height="45" viewBox="0 0 45 45" fill="none" xmlns="http://www.w3.org/2000/svg">\n    <g id="icons/article-image-right">\n        <rect id="icon-bg" width="45" height="45" rx="2" fill="#A5E7EB"/>\n        <g id="page" filter="url(#filter0_d_1_507)">\n            <path d="M9 41H36V12L28 5H9V41Z" fill="white"/>\n            <path d="M35.25 12.3403V40.25H9.75V5.75H27.7182L35.25 12.3403Z" stroke="#333333" stroke-width="1.5"/>\n        </g>\n        <g id="image">\n            <path id="Rectangle 22" d="M21.5 23C21.5 22.1716 22.1716 21.5 23 21.5H31C31.8284 21.5 32.5 22.1716 32.5 23V29C32.5 29.8284 31.8284 30.5 31 30.5H23C22.1716 30.5 21.5 29.8284 21.5 29V23Z" fill="#B6E3FC" stroke="#333333"/>\n            <path id="Vector 1" d="M24.1184 27.8255C23.9404 27.7499 23.7347 27.7838 23.5904 27.9125L21.6673 29.6268C21.5124 29.7648 21.4589 29.9842 21.5328 30.178C21.6066 30.3719 21.7925 30.5 22 30.5H32C32.2761 30.5 32.5 30.2761 32.5 30V27.7143C32.5 27.5717 32.4391 27.4359 32.3327 27.3411L30.4096 25.6268C30.2125 25.451 29.9127 25.4589 29.7251 25.6448L26.5019 28.8372L24.1184 27.8255Z" fill="#44D500" stroke="#333333" stroke-linejoin="round"/>\n            <circle id="Ellipse 1" cx="26" cy="25" r="1.5" fill="#FFD12D" stroke="#333333"/>\n        </g>\n        <rect id="Rectangle 23" x="13" y="13" width="12" height="2" rx="1" fill="#B4B4B4"/>\n        <rect id="Rectangle 24" x="13" y="17" width="19" height="2" rx="1" fill="#B4B4B4"/>\n        <rect id="Rectangle 25" x="13" y="21" width="6" height="2" rx="1" fill="#B4B4B4"/>\n        <rect id="Rectangle 26" x="13" y="25" width="6" height="2" rx="1" fill="#B4B4B4"/>\n        <rect id="Rectangle 27" x="13" y="29" width="6" height="2" rx="1" fill="#B4B4B4"/>\n        <rect id="Rectangle 28" x="13" y="33" width="16" height="2" rx="1" fill="#B4B4B4"/>\n    </g>\n    <defs>\n        <filter id="filter0_d_1_507" x="9" y="5" width="28" height="37" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">\n            <feFlood flood-opacity="0" result="BackgroundImageFix"/>\n            <feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>\n            <feOffset dx="1" dy="1"/>\n            <feComposite in2="hardAlpha" operator="out"/>\n            <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.29 0"/>\n            <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_1_507"/>\n            <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_1_507" result="shape"/>\n        </filter>\n    </defs>\n</svg>\n',
						data: "<h2>Introduction</h2><p>In today's fast-paced world, keeping up with the latest trends and insights is essential for both personal growth and professional development. This article aims to shed light on a topic that resonates with many, providing valuable information and actionable advice. Whether you're seeking to enhance your knowledge, improve your skills, or simply stay informed, our comprehensive analysis offers a deep dive into the subject matter, designed to empower and inspire our readers.</p>"
					}
				]
			}
		};
	}, [currentMergeFields, dataSets, initialData, selectedTemplate]);

	// Update editorConfig when currentMergeFields changes
	useEffect(() => {
		if (editorRef.current && editorRef.current.editor && currentMergeFields.length > 0) {
			const editor = editorRef.current.editor;
			editor.plugins.get('MergeFields').setDefinitions(currentMergeFields);
		}
	}, [currentMergeFields]);

	const handleTemplateClick = useCallback(async (template) => {
		setSelectedTemplate(template.file);
		setShowTemplates(false);
		await loadCustomData(template.file);
	}, [loadCustomData]);

	return (
		<div>
			<MenuBar style={{ position: 'fixed', top: 0, left: 0, right: 0, zIndex: 1000 }}>
				{/* Ensure dropdown and buttons are rendering correctly */}
				<div>
					<MenuButton onClick={() => setShowTemplates(!showTemplates)}>
						Gestion des templates
					</MenuButton>
					<DropdownContent show={showTemplates}>
						{templates.map((template) => (
							<DropdownItem key={template.file} onClick={() => handleTemplateClick(template)}>
								{template.name}
							</DropdownItem>
						))}
					</DropdownContent>
				</div>
				<MenuButton onClick={() => setShowModal(true)}>
					Visualiser diplômes
				</MenuButton>
			</MenuBar>
			
			{/* Ensure ViewDiploma is rendering correctly */}
			<ViewDiploma
				show={showModal}
				onClose={() => setShowModal(false)}
				currentMergeFields={currentMergeFields}
				availableDataSets={availableDataSets}
				mergeFieldValues={mergeFieldValues}
				setMergeFieldValues={setMergeFieldValues}
				editorRef={editorRef}
			/>

			<MainContainer>
				<EditorWrapper>
					<EditorHeader>
						{isLoading && <p>Loading template...</p>}
					</EditorHeader>
					<EditorContent>
						<div className="editor-container" ref={editorContainerRef}>
							<div ref={editorRef}>
								{isLayoutReady && initialData && !isLoading && (
									<CKEditor
										key={selectedTemplate}
										editor={ClassicEditor}
										config={editorConfig}
										data={initialData}
										onReady={editor => {
											editorRef.current = editor;
											console.log('Editor is ready to use!', editor);
										}}
									/>
								)}
							</div>
						</div>
					</EditorContent>
				</EditorWrapper>
			</MainContainer>
		</div>
	);
}
