import React, { useState } from 'react';
import styled from 'styled-components';

// Styled components (you can move these to a separate file if desired)
const Modal = styled.div`
  display: ${props => props.show ? 'flex' : 'none'};
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
  justify-content: center;
  align-items: center;
`;

const ModalContent = styled.div`
  background-color: #fefefe;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
`;

const CloseButton = styled.span`
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
  &:hover { color: #000; }
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
`;

const Label = styled.label`
  margin-bottom: 5px;
  font-weight: bold;
`;

const Input = styled.input`
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
`;

const Select = styled.select`
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
`;

const Button = styled.button`
  padding: 10px 20px;
  background-color: #5DBE9D;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  &:hover { background-color: #4CA889; }
`;

const ViewDiploma = ({ 
  show, 
  onClose, 
  currentMergeFields, 
  availableDataSets, 
  mergeFieldValues, 
  setMergeFieldValues, 
  editorRef 
}) => {
  const [isCustomData, setIsCustomData] = useState(false);
  const [currentDataSet, setCurrentDataSet] = useState(null);

  const handleMergeFieldChange = (fieldId, value) => {
    setMergeFieldValues(prev => ({ ...prev, [fieldId]: value }));
  };

  const handleGenerateDiploma = (e) => {
    e.preventDefault();
    if (editorRef.current && editorRef.current.editor) {
      let mergedContent = editorRef.current.editor.getData();
      Object.entries(mergeFieldValues).forEach(([key, value]) => {
        const regex = new RegExp(`{{${key}}}`, 'g');
        mergedContent = mergedContent.replace(regex, value);
      });
      editorRef.current.editor.setData(mergedContent);
    }
    onClose();
  };

  const handleDataSetChange = (dataSetId) => {
    if (dataSetId === '') {
      setCurrentDataSet(null);
      setMergeFieldValues({});
      return;
    }
    const selectedDataSet = availableDataSets.find(ds => ds.id === dataSetId);
    if (selectedDataSet) {
      setCurrentDataSet(selectedDataSet);
      setMergeFieldValues(selectedDataSet.values);
    } else {
      setCurrentDataSet(null);
      setMergeFieldValues({});
    }
  };

  const toggleCustomData = () => {
    setIsCustomData(!isCustomData);
    if (!isCustomData) {
      setCurrentDataSet(null);
      setMergeFieldValues({});
    }
  };

  return (
    <Modal show={show}>
      <ModalContent>
        <CloseButton onClick={onClose}>&times;</CloseButton>
        <h2>Visualiser un diplôme</h2>
        <Form onSubmit={handleGenerateDiploma}>
          <FormGroup>
            <Label>
              <input
                type="checkbox"
                checked={isCustomData}
                onChange={toggleCustomData}
              />
              Entrer des données personnalisées
            </Label>
          </FormGroup>
          
          {!isCustomData && (
            <FormGroup>
              <Label htmlFor="dataSet">Sélectionner un jeu de données</Label>
              <Select 
                id="dataSet" 
                onChange={(e) => handleDataSetChange(e.target.value)} 
                value={currentDataSet?.id || ''}
                disabled={isCustomData}
              >
                <option value="">Choisir un diplomé</option>
                {availableDataSets.map(ds => (
                  <option key={ds.id} value={ds.id}>{ds.label}</option>
                ))}
              </Select>
            </FormGroup>
          )}
          
          {currentMergeFields.map(field => (
            <FormGroup key={field.id}>
              <Label htmlFor={field.id}>{field.label}</Label>
              <Input
                id={field.id}
                type={field.id === 'Date' ? 'date' : 'text'}
                value={mergeFieldValues[field.id] || ''}
                onChange={(e) => handleMergeFieldChange(field.id, e.target.value)}
                disabled={!isCustomData && !currentDataSet}
              />
            </FormGroup>
          ))}
          
          <Button type="submit">Visualiser</Button>
        </Form>
      </ModalContent>
    </Modal>
  );
};

export default ViewDiploma;